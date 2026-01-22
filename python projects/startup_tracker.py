# program from first day of class
# ChatGPT vers. 5.2
# Prompt: Create an appp that tracks every application that runs on windows startup, tracks the memory and cpu usage of each application throughout the duration of startup, and allows the user to remove it from the list of startup processes in one click. create the application using Python

import os
import re
import csv
import time
import shlex
import queue
import shutil
import subprocess
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import psutil
import tkinter as tk
from tkinter import ttk, messagebox


import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Relaunch as admin
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        " ".join([f'"{arg}"' for arg in sys.argv]),
        None,
        1
    )
    sys.exit(0)

# -----------------------------
# Helpers
# -----------------------------

def now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def expand_env(s: str) -> str:
    # Expand %VAR% style
    return os.path.expandvars(s)

def normalize_cmd(s: str) -> str:
    s = expand_env(s or "").strip().strip('"').strip()
    s = re.sub(r"\s+", " ", s).lower()
    return s

def best_guess_exe_from_cmd(cmd: str) -> Optional[str]:
    """
    Best-effort extraction of an executable path from a startup command.
    Handles quotes, env vars, and common patterns.
    """
    if not cmd:
        return None
    cmd = expand_env(cmd).strip()

    # If starts with quote, take quoted segment
    if cmd.startswith('"'):
        end = cmd.find('"', 1)
        if end > 1:
            return cmd[1:end]

    # Otherwise use shlex split (Windows-ish)
    try:
        parts = shlex.split(cmd, posix=False)
        if parts:
            return parts[0]
    except Exception:
        pass

    # Fallback: take up to first space
    return cmd.split(" ")[0] if cmd else None

def is_probably_logon_task(row: Dict[str, str]) -> bool:
    """
    Scheduled tasks filtering heuristic.
    """
    trig = (row.get("Triggers") or "").lower()
    # Common triggers include "At log on", "At startup"
    return ("at log on" in trig) or ("at startup" in trig)

def mb(x: int) -> float:
    return x / (1024 * 1024)

# -----------------------------
# Data model
# -----------------------------

@dataclass
class StartupItem:
    name: str
    source: str  # "Registry:HKCU Run", "StartupFolder:User", "TaskScheduler"
    command: str
    location: str  # registry path/value, file path, task name, etc.
    enabled: bool = True

    # Monitoring results (filled after monitoring)
    matched_pid: Optional[int] = None
    matched_proc_name: Optional[str] = None
    avg_cpu: Optional[float] = None
    peak_cpu: Optional[float] = None
    avg_mem_mb: Optional[float] = None
    peak_mem_mb: Optional[float] = None
    notes: str = ""

    # Internal matching fields
    norm_cmd: str = field(init=False)
    exe_guess: Optional[str] = field(init=False)

    def __post_init__(self):
        self.norm_cmd = normalize_cmd(self.command)
        self.exe_guess = best_guess_exe_from_cmd(self.command)
        if self.exe_guess:
            self.exe_guess = normalize_cmd(self.exe_guess)

# -----------------------------
# Startup enumeration
# -----------------------------

def enum_registry_run_items() -> List[StartupItem]:
    """
    Enumerate common Run keys.
    """
    items: List[StartupItem] = []
    try:
        import winreg
    except Exception:
        return items

    keys = [
        ("HKCU", winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        ("HKLM", winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
        ("HKLM", winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run"),
    ]

    for hive_name, hive, subkey in keys:
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as k:
                i = 0
                while True:
                    try:
                        val_name, val_data, _ = winreg.EnumValue(k, i)
                        i += 1
                        items.append(
                            StartupItem(
                                name=val_name,
                                source=f"Registry:{hive_name} Run",
                                command=str(val_data),
                                location=f"{hive_name}\\{subkey}::{val_name}",
                                enabled=True
                            )
                        )
                    except OSError:
                        break
        except PermissionError:
            items.append(
                StartupItem(
                    name=f"(Access denied) {hive_name}\\{subkey}",
                    source=f"Registry:{hive_name} Run",
                    command="",
                    location=f"{hive_name}\\{subkey}",
                    enabled=False
                )
            )
        except FileNotFoundError:
            continue
        except Exception:
            continue

    return items

def enum_startup_folder_items() -> List[StartupItem]:
    """
    Enumerate files in Startup folders (shortcuts, scripts, etc).
    """
    items: List[StartupItem] = []

    # Per-user and all-users startup folders
    user_startup = Path(os.environ.get("APPDATA", "")) / r"Microsoft\Windows\Start Menu\Programs\Startup"
    common_startup = Path(os.environ.get("PROGRAMDATA", "")) / r"Microsoft\Windows\Start Menu\Programs\Startup"

    folders = [
        ("StartupFolder:User", user_startup),
        ("StartupFolder:AllUsers", common_startup),
    ]

    for src, folder in folders:
        if folder.exists():
            for p in folder.iterdir():
                if p.is_file():
                    items.append(
                        StartupItem(
                            name=p.stem,
                            source=src,
                            command=str(p),
                            location=str(p),
                            enabled=True
                        )
                    )
        else:
            # no folder; ignore
            pass

    return items

def enum_scheduled_tasks() -> List[StartupItem]:
    """
    Best-effort: query schtasks and pick tasks that appear to run at logon/startup.
    Disabling uses schtasks /Change /DISABLE.
    """
    items: List[StartupItem] = []

    try:
        # CSV output is easier to parse than the default table
        cmd = ["schtasks", "/Query", "/FO", "CSV", "/V"]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0 or not proc.stdout.strip():
            return items

        # schtasks CSV can have an initial blank line sometimes
        lines = [ln for ln in proc.stdout.splitlines() if ln.strip()]
        reader = csv.DictReader(lines)
        for row in reader:
            task_name = row.get("TaskName") or ""
            status = (row.get("Status") or "").strip()
            task_to_run = (row.get("Task To Run") or "").strip()
            triggers = (row.get("Triggers") or "").strip()

            if not task_name:
                continue

            # Filter for likely startup/logon tasks
            if not is_probably_logon_task(row):
                continue

            enabled = (status.lower() != "disabled")
            items.append(
                StartupItem(
                    name=task_name,
                    source="TaskScheduler",
                    command=task_to_run if task_to_run else f"(See task) Triggers={triggers}",
                    location=task_name,
                    enabled=enabled
                )
            )
    except FileNotFoundError:
        # schtasks not found (unlikely on Windows)
        return items
    except Exception:
        return items

    return items

def enumerate_all_startup_items() -> List[StartupItem]:
    items = []
    items.extend(enum_registry_run_items())
    items.extend(enum_startup_folder_items())
    items.extend(enum_scheduled_tasks())
    # Deduplicate by (source, location)
    seen = set()
    deduped = []
    for it in items:
        key = (it.source, it.location)
        if key not in seen:
            seen.add(key)
            deduped.append(it)
    return deduped

# -----------------------------
# Disable/remove actions
# -----------------------------

def disable_item(item: StartupItem, backup_dir: Path) -> Tuple[bool, str]:
    """
    Disables/removes startup entry depending on source.
    Returns (success, message).
    """
    # Registry removal
    if item.source.startswith("Registry:"):
        try:
            import winreg
            # location: "HKCU\...\Run::ValueName"
            loc = item.location
            if "::" not in loc:
                return False, "Invalid registry location format."
            hive_part, rest = loc.split("\\", 1)
            key_path, value_name = rest.split("::", 1)

            hive = winreg.HKEY_CURRENT_USER if hive_part == "HKCU" else winreg.HKEY_LOCAL_MACHINE

            # Need write access to delete value
            with winreg.OpenKey(hive, key_path, 0, winreg.KEY_SET_VALUE) as k:
                winreg.DeleteValue(k, value_name)

            return True, f"Removed registry Run entry: {value_name}"
        except PermissionError:
            return False, "Permission denied. Try running as Administrator."
        except FileNotFoundError:
            return False, "Registry key/value not found (already removed?)."
        except Exception as e:
            return False, f"Registry removal failed: {e}"

    # Startup folder removal (move to backup)
    if item.source.startswith("StartupFolder:"):
        try:
            p = Path(item.location)
            if not p.exists():
                return False, "Startup file not found (already removed?)."

            backup_dir.mkdir(parents=True, exist_ok=True)
            dest = backup_dir / p.name
            # Avoid overwrite
            if dest.exists():
                dest = backup_dir / f"{p.stem}_{now_str()}{p.suffix}"

            shutil.move(str(p), str(dest))
            return True, f"Moved startup file to backup: {dest}"
        except PermissionError:
            return False, "Permission denied. Try running as Administrator."
        except Exception as e:
            return False, f"File move failed: {e}"

    # Scheduled task disable
    if item.source == "TaskScheduler":
        try:
            # Disable task
            cmd = ["schtasks", "/Change", "/TN", item.location, "/DISABLE"]
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if proc.returncode == 0:
                return True, f"Disabled scheduled task: {item.location}"
            else:
                msg = proc.stderr.strip() or proc.stdout.strip() or "Unknown error."
                return False, f"Failed to disable task: {msg}"
        except PermissionError:
            return False, "Permission denied. Try running as Administrator."
        except Exception as e:
            return False, f"Task disable failed: {e}"

    return False, "Unsupported item type."

# -----------------------------
# Monitoring logic
# -----------------------------

def build_process_index() -> List[Dict]:
    """
    Snapshot current processes into dicts for matching.
    """
    procs = []
    for p in psutil.process_iter(attrs=["pid", "name", "exe", "cmdline"]):
        try:
            info = p.info
            exe = info.get("exe") or ""
            cmdline = " ".join(info.get("cmdline") or [])
            procs.append({
                "pid": info["pid"],
                "name": info.get("name") or "",
                "exe": normalize_cmd(exe),
                "cmd": normalize_cmd(cmdline),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        except Exception:
            continue
    return procs

def match_item_to_process(item: StartupItem, proc_index: List[Dict]) -> Optional[int]:
    """
    Best-effort match:
    - If we can guess exe, try match exe substring
    - Else match by command substring
    - Else fallback by name match (item name)
    """
    exe_guess = item.exe_guess or ""
    cmd_norm = item.norm_cmd or ""
    name_norm = normalize_cmd(item.name)

    # Prefer exact-ish exe match if it looks like a path
    if exe_guess and (".exe" in exe_guess or "\\" in exe_guess):
        for pr in proc_index:
            if pr["exe"] and exe_guess in pr["exe"]:
                return pr["pid"]

    # Try match by command text
    if cmd_norm and len(cmd_norm) >= 6:
        for pr in proc_index:
            if pr["cmd"] and cmd_norm[:20] in pr["cmd"]:
                return pr["pid"]

    # Fallback by process name containing item name
    if name_norm and len(name_norm) >= 3:
        for pr in proc_index:
            if name_norm in normalize_cmd(pr["name"]):
                return pr["pid"]

    return None

def monitor_items(items: List[StartupItem], duration_s: int, sample_interval: float, progress_cb=None) -> None:
    """
    Monitors CPU/mem for matched processes over duration window.
    Writes results into each StartupItem.
    """
    # Prepare per-item tracking
    tracked: Dict[int, Dict] = {}  # pid -> stats
    pid_to_item: Dict[int, StartupItem] = {}

    start = time.time()
    end = start + duration_s

    # Prime cpu_percent for existing processes
    for p in psutil.process_iter():
        try:
            p.cpu_percent(interval=None)
        except Exception:
            pass

    # Sampling loop
    samples_taken = 0
    while time.time() < end:
        t = time.time()

        # rebuild index occasionally for processes that appear after monitoring starts
        proc_index = build_process_index()

        # match items that don't have a pid yet
        for it in items:
            if not it.enabled:
                continue
            if it.matched_pid is None:
                pid = match_item_to_process(it, proc_index)
                if pid is not None:
                    it.matched_pid = pid
                    # Get name if possible
                    try:
                        it.matched_proc_name = psutil.Process(pid).name()
                    except Exception:
                        it.matched_proc_name = None

                    tracked[pid] = {
                        "cpu_sum": 0.0,
                        "cpu_peak": 0.0,
                        "mem_sum": 0.0,
                        "mem_peak": 0.0,
                        "n": 0
                    }
                    pid_to_item[pid] = it

        # sample tracked pids
        dead_pids = []
        for pid, st in list(tracked.items()):
            try:
                p = psutil.Process(pid)
                cpu = p.cpu_percent(interval=None)  # percent since last call
                mem = p.memory_info().rss

                st["cpu_sum"] += cpu
                st["cpu_peak"] = max(st["cpu_peak"], cpu)
                st["mem_sum"] += mem
                st["mem_peak"] = max(st["mem_peak"], mem)
                st["n"] += 1
            except (psutil.NoSuchProcess, psutil.ZombieProcess):
                dead_pids.append(pid)
            except psutil.AccessDenied:
                # keep but annotate
                pid_to_item[pid].notes = "AccessDenied during sampling (some stats may be missing)."
            except Exception:
                pass

        for pid in dead_pids:
            tracked.pop(pid, None)

        samples_taken += 1
        if progress_cb:
            progress_cb(min(1.0, (time.time() - start) / duration_s), samples_taken)

        # sleep to next interval
        elapsed = time.time() - t
        to_sleep = max(0.0, sample_interval - elapsed)
        time.sleep(to_sleep)

    # Finalize stats into items
    for pid, st in tracked.items():
        it = pid_to_item.get(pid)
        if not it:
            continue
        n = max(1, st["n"])
        it.avg_cpu = st["cpu_sum"] / n
        it.peak_cpu = st["cpu_peak"]
        it.avg_mem_mb = mb(st["mem_sum"] / n)
        it.peak_mem_mb = mb(st["mem_peak"])

    # Items never matched
    for it in items:
        if it.enabled and it.matched_pid is None:
            it.notes = (it.notes + " " if it.notes else "") + "No matching process found during monitoring window."

# -----------------------------
# GUI
# -----------------------------

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Windows Startup Tracker (Python)")
        self.geometry("1250x650")

        self.items: List[StartupItem] = []
        self.item_by_iid: Dict[str, StartupItem] = {}

        self.ui_queue = queue.Queue()
        self.monitor_thread: Optional[threading.Thread] = None
        self.monitor_stop = threading.Event()

        self.backup_dir = Path.home() / "StartupTracker_Backups"

        self._build_ui()
        self.refresh()

        self.after(100, self._poll_ui_queue)

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(top, text="Refresh Startup List", command=self.refresh).pack(side="left")

        ttk.Label(top, text="  Monitor duration (sec):").pack(side="left")
        self.duration_var = tk.IntVar(value=120)
        ttk.Entry(top, textvariable=self.duration_var, width=8).pack(side="left")

        ttk.Label(top, text="  Sample interval (sec):").pack(side="left")
        self.interval_var = tk.DoubleVar(value=1.0)
        ttk.Entry(top, textvariable=self.interval_var, width=6).pack(side="left")

        ttk.Button(top, text="Start Monitoring", command=self.start_monitoring).pack(side="left", padx=8)

        self.progress = ttk.Progressbar(top, length=250, mode="determinate")
        self.progress.pack(side="left", padx=8)
        self.progress["value"] = 0

        ttk.Button(top, text="Disable Selected (One Click)", command=self.disable_selected).pack(side="right")

        # Tree/table
        cols = (
            "Name", "Source", "Enabled", "Command/Path", "PID", "ProcName",
            "AvgCPU%", "PeakCPU%", "AvgMemMB", "PeakMemMB", "Notes"
        )
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=22)
        for c in cols:
            self.tree.heading(c, text=c)
            # widths
            w = 120
            if c in ("Command/Path", "Notes"):
                w = 420 if c == "Command/Path" else 260
            if c in ("AvgCPU%", "PeakCPU%", "AvgMemMB", "PeakMemMB", "PID"):
                w = 90
            if c in ("Enabled",):
                w = 70
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Bottom help
        bottom = ttk.Frame(self)
        bottom.pack(fill="x", padx=10, pady=(0,10))
        ttk.Label(
            bottom,
            text=(
                "Tip: Run as Administrator to disable HKLM Run entries and some scheduled tasks. "
                f"Startup-folder removals are backed up to: {self.backup_dir}"
            )
        ).pack(side="left")

    def refresh(self):
        self.items = enumerate_all_startup_items()
        self._render_items()

    def _render_items(self):
        self.tree.delete(*self.tree.get_children())
        self.item_by_iid.clear()

        for it in self.items:
            iid = str(id(it))
            self.item_by_iid[iid] = it
            self.tree.insert("", "end", iid=iid, values=self._row_values(it))

    def _row_values(self, it: StartupItem):
        def fmt(x, digits=2):
            return "" if x is None else f"{x:.{digits}f}"

        return (
            it.name,
            it.source,
            "Yes" if it.enabled else "No",
            it.command,
            "" if it.matched_pid is None else str(it.matched_pid),
            it.matched_proc_name or "",
            fmt(it.avg_cpu, 2),
            fmt(it.peak_cpu, 2),
            fmt(it.avg_mem_mb, 2),
            fmt(it.peak_mem_mb, 2),
            it.notes or ""
        )

    def start_monitoring(self):
        if self.monitor_thread and self.monitor_thread.is_alive():
            messagebox.showinfo("Monitoring", "Monitoring is already running.")
            return

        # Clear previous results
        for it in self.items:
            it.matched_pid = None
            it.matched_proc_name = None
            it.avg_cpu = None
            it.peak_cpu = None
            it.avg_mem_mb = None
            it.peak_mem_mb = None
            it.notes = ""

        self._render_items()
        self.progress["value"] = 0

        duration = max(10, int(self.duration_var.get() or 120))
        interval = max(0.25, float(self.interval_var.get() or 1.0))

        def progress_cb(frac, samples):
            self.ui_queue.put(("progress", frac))

        def worker():
            try:
                monitor_items(self.items, duration, interval, progress_cb=progress_cb)
                self.ui_queue.put(("done", None))
            except Exception as e:
                self.ui_queue.put(("error", str(e)))

        self.monitor_thread = threading.Thread(target=worker, daemon=True)
        self.monitor_thread.start()

    def disable_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Disable", "Select at least one startup entry.")
            return

        # Confirm
        if not messagebox.askyesno(
            "Confirm Disable",
            "This will disable/remove the selected startup entries.\n\n"
            "Registry Run entries will be deleted.\n"
            "Startup-folder files will be moved to a backup folder.\n"
            "Scheduled tasks will be disabled.\n\nProceed?"
        ):
            return

        ok_count = 0
        msgs = []

        for iid in sel:
            it = self.item_by_iid.get(iid)
            if not it:
                continue
            if not it.enabled:
                msgs.append(f"{it.name}: already disabled / unavailable.")
                continue

            success, msg = disable_item(it, self.backup_dir)
            if success:
                ok_count += 1
                it.enabled = False
                it.notes = msg
            else:
                it.notes = msg
                msgs.append(f"{it.name}: {msg}")

        self._render_items()
        if msgs:
            messagebox.showwarning("Some actions failed", "\n".join(msgs[:20]) + ("\n..." if len(msgs) > 20 else ""))
        else:
            messagebox.showinfo("Disable", f"Disabled/removed {ok_count} item(s).")

    def _poll_ui_queue(self):
        try:
            while True:
                kind, payload = self.ui_queue.get_nowait()
                if kind == "progress":
                    self.progress["value"] = payload * 100
                elif kind == "done":
                    self.progress["value"] = 100
                    self._render_items()
                    messagebox.showinfo("Monitoring", "Monitoring complete. Stats updated in the table.")
                elif kind == "error":
                    messagebox.showerror("Error", f"Monitoring error:\n{payload}")
        except queue.Empty:
            pass
        self.after(100, self._poll_ui_queue)

if __name__ == "__main__":
    app = App()
    app.mainloop()
