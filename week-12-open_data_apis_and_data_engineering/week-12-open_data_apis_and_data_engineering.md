# Week 12: Open Data APIs & Data Engineering

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 12 of 16 | **Date:** 2026-05-14 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Explain REST API basics: endpoint, GET request, JSON response, HTTP status codes
2. Make HTTP requests with `requests.get()` and parse JSON into a DataFrame
3. Find usable datasets on data.gov.tw and the Taiwan EPA open data portal
4. Handle API errors and missing responses gracefully
5. Clean a real dataset with `dropna()`, `fillna()`, `astype()`, and `to_datetime()`
6. Join two DataFrames on a common key with `pd.merge()`
7. Cache API responses locally to avoid redundant network calls during development

---

## In-Class Topics

### 1. REST API Basics (15 min)

A REST API lets you retrieve data from a server by sending an HTTP GET request to a URL. The server responds with JSON.

```
Request:  GET https://api.example.com/data?city=Taipei&limit=100
Response: { "status": "ok", "records": [ { "date": "2024-01-01", "pm25": 22 }, ... ] }
```

Key concepts:

| Term | Meaning |
|------|---------|
| Endpoint | The URL you request |
| Query parameter | `?key=value` appended to the URL to filter results |
| Status code | `200` = OK, `404` = not found, `429` = rate limited |
| JSON | The response format — maps directly to Python dicts and lists |

---

### 2. Making a Request with `requests` (20 min)

```python
import requests
import pandas as pd

url    = "https://data.epa.gov.tw/api/v2/aqx_p_432"
params = {
    "api_key": "YOUR_API_KEY",   # register free at data.epa.gov.tw
    "limit":   1000,
    "format":  "json",
}

response = requests.get(url, params=params, timeout=10)

# Always check the status code before using the response
if response.status_code != 200:
    raise ValueError(f"API returned status {response.status_code}")

data = response.json()
print(data.keys())          # see the top-level structure
print(data["records"][:2])  # preview first two records

df = pd.DataFrame(data["records"])
print(df.shape)
print(df.dtypes)
```

`timeout=10` prevents your program from hanging forever if the server does not respond. Always include it.

---

### 3. Navigating Taiwan Open Data Portals (20 min)

**data.gov.tw** — general government open data:

```python
# Example: hospital locations dataset
url    = "https://data.gov.tw/api/v1/rest/datastore/5765a74e-edd5-4f54-a0e5-57739fae7b04"
params = {"limit": 100, "offset": 0}

r  = requests.get(url, params=params, timeout=10)
df = pd.DataFrame(r.json()["result"]["records"])
```

The portal at data.gov.tw lists thousands of datasets. The dataset ID appears in the URL when you open a dataset page. Most datasets provide a direct download CSV link as well as a JSON API.

**EPA open data portal** — environmental data including air quality, water quality, and noise:

```python
# AQI (Air Quality Index) by monitoring station — real-time
url = "https://data.epa.gov.tw/api/v2/aqx_p_432"
# Documentation: https://data.epa.gov.tw/en/dataset/aqx_p_432
```

**Recommended datasets for final projects:**

| Topic | Portal | Dataset name |
|-------|--------|--------------|
| Air quality (PM2.5, AQI) | EPA | `aqx_p_432` — hourly AQI by station |
| Earthquake records | CWA | Central Weather Administration open data |
| Hospital distribution | data.gov.tw | Medical institution locations |
| Transit ridership | data.gov.tw | MRT / TRA daily passengers |
| Water quality | EPA | River water quality monitoring |

---

### 4. Pandas Data Cleaning (30 min)

Real datasets almost always need cleaning before they can be analysed or displayed.

**Step 1 — Inspect the raw data:**
```python
print(df.shape)
print(df.dtypes)
print(df.isnull().sum())
print(df.head(3))
```

**Step 2 — Fix column types:**
```python
# Convert numeric columns stored as strings
df["pm25"]  = pd.to_numeric(df["pm25"],  errors="coerce")   # invalid → NaN
df["aqi"]   = pd.to_numeric(df["aqi"],   errors="coerce")

# Parse date/time strings
df["date"]  = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
df["time"]  = pd.to_datetime(df["time"], format="%H:%M",    errors="coerce")
```

`errors="coerce"` turns unparsable values into `NaN` rather than raising an exception — essential for messy real-world data.

**Step 3 — Handle missing values:**
```python
print(f"Rows before: {len(df)}")
df = df.dropna(subset=["pm25", "date"])   # drop rows where these columns are NaN
print(f"Rows after dropna: {len(df)}")

# Fill NaN in categorical columns
df["station"] = df["station"].fillna("Unknown")

# Forward-fill a time series (carry last valid value forward)
df = df.sort_values("date")
df["pm25"] = df["pm25"].fillna(method="ffill")
```

**Step 4 — Filter and validate:**
```python
# Remove physically implausible values
df = df[(df["pm25"] >= 0) & (df["pm25"] <= 500)]

# Keep only the columns you need
df = df[["date", "station", "county", "pm25", "aqi"]]
```

---

### 5. Merging DataFrames (20 min)

Joining two datasets on a shared key is one of the most common data engineering operations.

```python
# Dataset 1: air quality readings (station-level)
aq = pd.read_csv("data/air_quality.csv")   # columns: station_id, date, pm25

# Dataset 2: station metadata (location, county)
stations = pd.read_csv("data/stations.csv")  # columns: station_id, station_name, county, lat, lon

# Inner join — keep only rows where station_id exists in both DataFrames
merged = pd.merge(aq, stations, on="station_id", how="inner")

# Left join — keep all rows from aq, fill missing station info with NaN
merged = pd.merge(aq, stations, on="station_id", how="left")

print(merged.columns.tolist())
print(merged.head(3))
```

Use `how="left"` when you want to keep all your measurement records even if the station metadata is incomplete.

---

### 6. Caching API Responses During Development (10 min)

Repeatedly calling an API during development is slow and may hit rate limits. Cache the response to a local file and reload from it if the file exists.

```python
import os
import json

CACHE_FILE = "data/aq_raw.json"

def fetch_or_load(url: str, params: dict, cache_file: str) -> list:
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    records = response.json()["records"]

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    return records
```

Delete the cache file when you want fresh data. In production (on Streamlit Cloud), you will use `@st.cache_data` with a `ttl` parameter instead.

---

## Course Connection

| This week | Connection to final project |
|-----------|----------------------------|
| `requests.get()` | Fetch live data from a Taiwan open data API in your Streamlit app |
| JSON → DataFrame | Convert API response into a pandas table for display and charting |
| `dropna`, `astype` | Ensure data is clean before passing to Plotly or Matplotlib |
| `pd.merge()` | Combine readings with station metadata to enable geographic filtering |
| Local cache | Develop and test without hitting API rate limits |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| `requests` | HTTP requests | `pip install requests` |
| pandas | Data cleaning and merging | `pip install pandas` |
| data.gov.tw | Taiwan government open data portal | [data.gov.tw/en](https://data.gov.tw/en) |
| EPA open data | Environmental data API | [data.epa.gov.tw/en](https://data.epa.gov.tw/en) |

---

## Assignment

Add a live data fetch to your Streamlit project:

1. Identify the API endpoint for your chosen dataset on data.gov.tw or the EPA portal.
2. Write a `utils/fetch_data.py` function that:
   - Calls the API using `requests.get()` with appropriate query parameters
   - Returns a cleaned pandas DataFrame (correct dtypes, no obvious nulls in key columns)
   - Caches the response locally for development
3. Apply at least three cleaning operations (`to_numeric`, `to_datetime`, `dropna` or `fillna`) and document what each one fixes.
4. If your project uses two related datasets, merge them with `pd.merge()` and show the merged table in your Streamlit app.
5. Write one pytest test that checks your cleaning function handles a missing value correctly.

Submit the updated GitHub repository URL on the course portal before Week 13.

---

## Resources

- [requests library documentation](https://requests.readthedocs.io/)
- [pandas cleaning guide](https://pandas.pydata.org/docs/user_guide/missing_data.html)
- [pandas merge documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html)
- [data.gov.tw English portal](https://data.gov.tw/en)
- [Taiwan EPA open data portal](https://data.epa.gov.tw/en/)
- [Central Weather Administration open data](https://opendata.cwa.gov.tw/en)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 13 | Interactive dashboards — Plotly Express charts and data storytelling |
| 14 | AI features — call the Claude API from inside your Streamlit app |
| 15 | Final project workshop — peer review and UI polish |
| 16 | **Final milestone:** Live app presentation |
