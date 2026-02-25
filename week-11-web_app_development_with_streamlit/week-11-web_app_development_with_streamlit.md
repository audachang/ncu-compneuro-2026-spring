# Week 11: Web App Development with Streamlit

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 11 of 16 | **Date:** 2026-05-07 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Build a multi-section Streamlit app with titles, markdown, and dataframe displays
2. Add interactive widgets: slider, selectbox, and file uploader
3. Display static Matplotlib charts and Streamlit's built-in line chart
4. Organize a page using columns and a sidebar
5. Apply `@st.cache_data` to prevent expensive data loads from re-running on every interaction
6. Deploy a Streamlit app to Streamlit Cloud from a GitHub repository

---

## In-Class Topics

### 1. The Streamlit Model (10 min)

Streamlit reruns your entire `app.py` script from top to bottom every time the user interacts with a widget. This means:

- No callbacks or event handlers — just write Python top to bottom
- Every widget call returns the current value immediately
- Use `@st.cache_data` to prevent expensive operations from repeating unnecessarily

```bash
pip install streamlit
streamlit run app.py
```

The app opens at `http://localhost:8501` and updates live as you save the file.

---

### 2. Basic Display Functions (15 min)

```python
import streamlit as st
import pandas as pd
import numpy as np

st.title("Taiwan Air Quality Dashboard")
st.write("This app shows PM2.5 levels across monitoring stations.")

# Markdown with inline formatting
st.markdown("**Data source:** Environmental Protection Administration open data portal")

# Display a DataFrame as an interactive table
df = pd.read_csv("data/air_quality.csv")
st.dataframe(df.head(20))

# Key metrics in a row
col1, col2, col3 = st.columns(3)
col1.metric("Stations",     df["station"].nunique())
col2.metric("Days covered", df["date"].nunique())
col3.metric("Mean PM2.5",   f"{df['pm25'].mean():.1f} µg/m³")
```

`st.metric()` renders a large number with an optional delta arrow — useful for summary statistics at the top of a dashboard.

---

### 3. Widgets (25 min)

**Selectbox:**
```python
stations  = sorted(df["station"].unique())
selected  = st.selectbox("Select a monitoring station", stations)
df_filtered = df[df["station"] == selected]
```

**Slider:**
```python
pm25_threshold = st.slider(
    "PM2.5 alert threshold (µg/m³)",
    min_value=0,
    max_value=150,
    value=35,       # default
    step=5,
)

n_exceeding = (df["pm25"] > pm25_threshold).sum()
st.write(f"{n_exceeding} readings exceed {pm25_threshold} µg/m³")
```

**File uploader:**
```python
uploaded = st.file_uploader("Upload your own CSV", type="csv")

if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    st.dataframe(user_df)
    st.success(f"Loaded {len(user_df)} rows.")
```

Streamlit renders these widgets in the order they appear in the script. Changing any widget reruns the script — the `selected` and `pm25_threshold` variables automatically reflect the new values.

---

### 4. Charts (20 min)

**Built-in line chart (quick):**
```python
df_station = df[df["station"] == selected].set_index("date")
st.line_chart(df_station["pm25"])
```

**Matplotlib figure (more control):**
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(df_station.index, df_station["pm25"], color="steelblue", linewidth=1.5)
ax.axhline(35, color="orange", linestyle="--", label="WHO guideline (35 µg/m³)")
ax.set_xlabel("Date")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_title(f"PM2.5 at {selected}")
ax.legend()
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
```

Use `st.pyplot(fig)` (not `plt.show()`) inside a Streamlit app.

---

### 5. Layout — Columns and Sidebar (15 min)

**Two-column layout:**
```python
left, right = st.columns([2, 1])   # 2:1 width ratio

with left:
    st.subheader("PM2.5 over time")
    st.line_chart(df_station["pm25"])

with right:
    st.subheader("Summary statistics")
    st.write(df_station["pm25"].describe().round(1))
```

**Sidebar — filters that do not take up main column space:**
```python
with st.sidebar:
    st.header("Filters")
    selected_station = st.selectbox("Station", stations)
    date_range       = st.date_input("Date range", [])
    show_guideline   = st.checkbox("Show WHO guideline (35 µg/m³)", value=True)
```

Sidebar widgets work exactly like regular widgets — they just appear in the left panel.

---

### 6. Caching with `@st.cache_data` (15 min)

Without caching, the CSV is read from disk on every widget interaction. For a large dataset, this causes noticeable lag.

```python
@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath, parse_dates=["date"])
    df["pm25"] = pd.to_numeric(df["pm25"], errors="coerce")
    df = df.dropna(subset=["pm25"])
    return df

df = load_data("data/air_quality.csv")
```

`@st.cache_data` stores the return value keyed by the function arguments. The CSV is only read once per session — or when the file path changes.

Use `@st.cache_data` on any function that:
- reads a file or makes a network request
- computes something that takes more than a few milliseconds

---

### 7. Deploying to Streamlit Cloud (15 min)

1. Push your project to a public GitHub repository.
2. Your repository must contain:
   - `app.py` (or another `.py` file you specify)
   - `requirements.txt` listing all dependencies

```
# requirements.txt
streamlit>=1.33
pandas>=2.0
matplotlib>=3.8
```

3. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
4. Click **New app**, select your repository, branch, and file path.
5. Click **Deploy**. Streamlit Cloud builds the environment and starts the app.

The deployed URL is permanent and publicly shareable. This is the URL you will present in Week 16.

---

## Course Connection

| Concept | Application in this course |
|---------|---------------------------|
| `st.selectbox` | Let users filter data by city or variable |
| `@st.cache_data` | Cache the Taiwan open data API response |
| `st.columns` | Side-by-side chart and summary table |
| `st.sidebar` | Keep filter controls out of the main content area |
| Streamlit Cloud | Host your final project publicly for Week 16 presentation |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| Streamlit | Web app framework | `pip install streamlit` |
| Streamlit Cloud | Free app hosting | [share.streamlit.io](https://share.streamlit.io) |
| pandas | Data loading and manipulation | `pip install pandas` |
| matplotlib | Static charts inside Streamlit | `pip install matplotlib` |

---

## Assignment

Build a working Streamlit prototype for your final project and deploy it to Streamlit Cloud.

**Requirements:**

1. Load your Taiwan open dataset (from Week 09) using a cached function.
2. Include at least two widgets (e.g., a selectbox to filter by region and a slider to set a threshold).
3. Display a Matplotlib or built-in chart that responds to the widget selections.
4. Show a summary statistics table below the chart.
5. Organize the layout with `st.columns()` or a `st.sidebar`.
6. Deploy to Streamlit Cloud and confirm the URL is publicly accessible.

Submit the Streamlit Cloud URL and the GitHub repository URL on the course portal before Week 12.

---

## Resources

- [Streamlit documentation](https://docs.streamlit.io/)
- [Streamlit cheat sheet](https://cheat-sheet.streamlit.app/)
- [Streamlit API reference — all widgets](https://docs.streamlit.io/develop/api-reference/widgets)
- [Streamlit caching guide](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [Streamlit Cloud deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 12 | Open data APIs — fetch live data from data.gov.tw and the EPA portal |
| 13 | Interactive charts with Plotly Express and data storytelling |
| 14 | Add an AI feature using the Claude API |
| 16 | **Final milestone:** Present your polished, deployed web app |
