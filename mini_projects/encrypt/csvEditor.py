import pandas as pd
import hashlib

def hash(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()  # 64 hex chars = 32 bytes

setwd = 'C:/Users/fmcgowan1/OneDrive - Babson College/02 Spring 2026/OIM 3640/public-repository/mini_projects/encrypt'
df = pd.read_csv(setwd + '/words.csv')

for i in range(len(df)):
    df['key'][i] = hash(df['word'][i])
    
print(df.head())]