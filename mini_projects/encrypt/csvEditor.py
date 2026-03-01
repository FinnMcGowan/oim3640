import os
import pandas as pd
import hashlib

def hash(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()  # 64 hex chars = 32 bytes

# construct a path; you can also just hard‑code the relative location
setwd = 'C:/Users/fmcgowan1/OneDrive - Babson College/02 Spring 2026/OIM 3640/public-repository/mini_projects/encrypt'
df = pd.read_csv(setwd + '/words.csv')

# words.csv contains a stray empty row, so ``aa`` has a NaN.
# ``hash`` assumes a string and fails when it sees a float, so
# either drop or coerce before applying.  here we'll just cast
to str (NaN becomes 'nan')
# alternatively: df = df.dropna(subset=['aa'])
df['aa'] = df['aa'].astype(str)

# create the new column in one shot rather than looping
# the assignment below works even if ``key`` doesn't yet exist
# using ``apply`` is vectorised and much faster than iterating
# over rows; there is no need to use ``for i in range(...)``
df['key'] = df['Word'].apply(hash)

print(df.head())

# write the dataframe back out to a new file named words(1).csv
orig_path = setwd + '/words.csv'
base, ext = os.path.splitext(orig_path)
new_path = f"{base}_w_hash{ext}"
df.to_csv(new_path, index=False)
print(f"saved modified dataframe to {new_path}")

