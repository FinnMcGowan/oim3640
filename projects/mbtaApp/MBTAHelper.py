from pathlib import Path
import os

from flask import Flask, render_template, request
import requests


BASE_DIR = Path(__file__).resolve().parent.parent


def load_env_file(env_path):
	"""Load key=value pairs from a .env file into environment variables."""
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		key = key.strip()
		value = value.strip().strip('"').strip("'")

		if key and key not in os.environ:
			os.environ[key] = value


load_env_file(BASE_DIR / ".env")
MBTA_API_KEY = os.getenv("MBTA_API_KEY", "").strip()

app = Flask(__name__, template_folder=str(Path(__file__).resolve().parent))


def get_nearest_station(latitude, longitude):
	"""Return nearest MBTA stop for latitude/longitude, or (None, error_message)."""
	if not MBTA_API_KEY:
		return None, "MBTA API key is missing. Add MBTA_API_KEY in your .env file."

	url = "https://api-v3.mbta.com/stops"
	params = {
		"filter[latitude]": latitude,
		"filter[longitude]": longitude,
		"sort": "distance",
		"page[limit]": 1,
	}
	headers = {"x-api-key": MBTA_API_KEY}

	try:
		response = requests.get(url, params=params, headers=headers, timeout=10)
		response.raise_for_status()
	except requests.RequestException:
		return None, "Could not reach MBTA API right now. Please try again."

	payload = response.json()
	data = payload.get("data") or []
	if not data:
		return None, "No nearby MBTA stations were found for those coordinates."

	station = data[0]
	attributes = station.get("attributes") or {}

	return {
		"name": attributes.get("name", "Unknown Station"),
		"municipality": attributes.get("municipality", "Unknown Municipality"),
		"address": attributes.get("address", "Address not available"),
	}, None


def geocode_place(place_query):
	"""Convert a place name (for example, Boston Common) into latitude/longitude."""
	url = "https://nominatim.openstreetmap.org/search"
	params = {
		"q": place_query,
		"format": "json",
		"limit": 1,
	}
	headers = {"User-Agent": "mbta-station-finder/1.0"}

	response = requests.get(url, params=params, headers=headers, timeout=10)
	response.raise_for_status()

	results = response.json()
	if not results:
		return None

	first = results[0]
	return {
		"latitude": float(first["lat"]),
		"longitude": float(first["lon"]),
		"display_name": first.get("display_name", place_query),
	}


@app.get("/")
def home():
	return render_template("StationFinder.html", result=None, error=None, place="", looked_up_place=None)


@app.post("/nearest-station")
def nearest_station():
	place = request.form.get("place", "").strip()
	if not place:
		return render_template(
			"StationFinder.html",
			result=None,
			error="Please enter your location (for example: Boston Common).",
			place="",
			looked_up_place=None,
		)

	try:
		geo = geocode_place(place)
		if geo is None:
			return render_template(
				"StationFinder.html",
				result=None,
				error="Could not understand that location. Try a more specific place name.",
				place=place,
				looked_up_place=None,
			)

		station, error = get_nearest_station(geo["latitude"], geo["longitude"])
		return render_template(
			"StationFinder.html",
			result=station,
			error=error,
			place=place,
			looked_up_place=geo["display_name"],
		)
	except requests.RequestException:
		return render_template(
			"StationFinder.html",
			result=None,
			error="Could not reach the location or MBTA service. Please try again.",
			place=place,
			looked_up_place=None,
		)


if __name__ == "__main__":
	app.run(debug=True)
