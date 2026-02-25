# Week 13: Interactive Dashboards & Data Storytelling

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 13 of 16 | **Date:** 2026-05-21 | **Room:** TBA

---

## Learning Objectives

By the end of this week you will be able to:

1. Create bar, scatter, line, and choropleth maps with Plotly Express
2. Configure hover labels, color scales, and axis titles in Plotly figures
3. Add annotations to highlight a specific data point or event
4. Embed a Plotly figure in Streamlit with `st.plotly_chart()`
5. Describe the five principles of clear data storytelling and apply them to a chart
6. Produce a minimal Altair chart as an alternative to Plotly

---

## In-Class Topics

### 1. Why Plotly Instead of Matplotlib? (10 min)

Matplotlib produces publication-quality static images. Plotly produces interactive figures that work in a browser: users can hover to see values, zoom, pan, and click to filter. For a web dashboard, interactivity is a first-class feature.

```bash
pip install plotly
```

Plotly Express (`px`) is the high-level interface — one function call per chart type. The lower-level `plotly.graph_objects` (`go`) gives full control when you need it.

---

### 2. Bar Chart (15 min)

```python
import plotly.express as px
import pandas as pd

# Mean PM2.5 per county, sorted descending
county_avg = (
    df.groupby("county")["pm25"]
    .mean()
    .reset_index()
    .sort_values("pm25", ascending=False)
)

fig = px.bar(
    county_avg,
    x="county",
    y="pm25",
    color="pm25",
    color_continuous_scale="Reds",
    labels={"pm25": "Mean PM2.5 (µg/m³)", "county": "County"},
    title="Average PM2.5 by County",
)

fig.update_layout(coloraxis_showscale=False)
fig.show()   # in a script; use st.plotly_chart(fig) in Streamlit
```

`color_continuous_scale="Reds"` maps numeric values to a colour gradient — immediately communicates which bars are high.

---

### 3. Line Chart (15 min)

```python
# Daily PM2.5 for a selected station
fig = px.line(
    df_station,
    x="date",
    y="pm25",
    title=f"Daily PM2.5 — {selected_station}",
    labels={"date": "Date", "pm25": "PM2.5 (µg/m³)"},
    color_discrete_sequence=["steelblue"],
)

# Add a WHO guideline reference line
fig.add_hline(
    y=35,
    line_dash="dot",
    line_color="orange",
    annotation_text="WHO daily guideline (35 µg/m³)",
    annotation_position="top right",
)

fig.update_layout(hovermode="x unified")   # show all traces on hover
```

`hovermode="x unified"` groups tooltips by x-value — useful when comparing multiple lines.

---

### 4. Scatter Plot (15 min)

```python
# Relationship between PM2.5 and AQI across all stations
fig = px.scatter(
    df,
    x="pm25",
    y="aqi",
    color="county",
    size="pm25",
    hover_name="station",
    hover_data={"date": True, "pm25": ":.1f", "aqi": True},
    title="PM2.5 vs AQI by County",
    labels={"pm25": "PM2.5 (µg/m³)", "aqi": "AQI"},
    opacity=0.7,
)

fig.update_layout(legend_title_text="County")
```

`hover_data` controls exactly what appears in the tooltip. `hover_name` sets the bold title line in the tooltip.

---

### 5. Choropleth Map (20 min)

A choropleth map colours geographic regions by a numeric value. Plotly supports GeoJSON boundaries.

```python
import json
import requests

# Download Taiwan county GeoJSON (one-time)
geojson_url = "https://raw.githubusercontent.com/datasets/geo-admin1-tw/main/data/geo-admin1-tw.json"
geojson     = requests.get(geojson_url).json()

fig = px.choropleth_mapbox(
    county_avg,
    geojson=geojson,
    locations="county",
    featureidkey="properties.NAME_2",    # key in the GeoJSON that matches county column
    color="pm25",
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=6,
    center={"lat": 23.6, "lon": 121.0},
    title="Average PM2.5 by County",
    labels={"pm25": "PM2.5 (µg/m³)"},
)

fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
```

A free Mapbox token is not required when using `mapbox_style="carto-positron"` or `"open-street-map"`.

---

### 6. Annotations (15 min)

Annotations draw a reader's attention to what matters. Add them when a specific event or threshold has scientific or policy significance.

```python
# Mark the date a major pollution event occurred
fig.add_annotation(
    x="2024-01-15",
    y=85,
    text="Industrial fire — Jan 15",
    showarrow=True,
    arrowhead=2,
    arrowcolor="black",
    font=dict(size=11, color="black"),
    bgcolor="rgba(255,255,255,0.8)",
    bordercolor="black",
    borderwidth=1,
)
```

Annotations should explain *why* a value is notable, not just label the data point.

---

### 7. Embedding in Streamlit (10 min)

```python
import streamlit as st

# Plotly chart — interactive in the browser
st.plotly_chart(fig, use_container_width=True)

# use_container_width=True makes the chart expand to fill the column width
# Pass config to hide the Plotly toolbar (cleaner look for dashboards)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
```

`st.plotly_chart()` passes the Plotly figure object directly — no need to call `.show()` first.

---

### 8. Altair Basics (10 min)

Altair is a declarative charting library built on Vega-Lite. It produces interactive browser charts with very concise syntax.

```python
import altair as alt

chart = (
    alt.Chart(df_station)
    .mark_line()
    .encode(
        x=alt.X("date:T", title="Date"),
        y=alt.Y("pm25:Q", title="PM2.5 (µg/m³)"),
        tooltip=["date:T", "pm25:Q", "station:N"],
    )
    .properties(title=f"PM2.5 at {selected_station}", width=700, height=300)
    .interactive()
)

st.altair_chart(chart, use_container_width=True)
```

The `:T`, `:Q`, `:N` suffixes specify field types: temporal, quantitative, and nominal. Altair infers appropriate scales and axes from these types.

---

## Principles of Data Storytelling

A chart should communicate a single clear finding. These five principles apply to any visualization in a scientific or policy context:

| Principle | What it means | Common violation |
|-----------|--------------|-----------------|
| One message per chart | Each chart should answer exactly one question | Cramming four variables into one scatter plot |
| Context before detail | Show the big picture first, then drill down | Starting with a table of raw numbers |
| Label what matters | Annotate the point or line that is the main finding | Leaving readers to find the interesting value |
| Show uncertainty | Include error bars or confidence bands | Reporting a mean without any measure of spread |
| Earn the complexity | Only use maps or 3D when geography or three-way interaction is the point | Choropleth when a bar chart would be clearer |

---

## Tools This Week

| Tool | Purpose | Install |
|------|---------|---------|
| Plotly Express | Interactive charts | `pip install plotly` |
| Altair | Declarative interactive charts | `pip install altair` |
| Streamlit | Embed charts in a web app | `pip install streamlit` (from Week 11) |
| requests | Download GeoJSON boundaries | `pip install requests` (from Week 12) |

---

## Assignment

Add at least two interactive Plotly charts to your Streamlit app and apply data storytelling principles:

1. Add a `px.bar()` or `px.line()` chart that responds to at least one Streamlit widget.
2. Add a `px.scatter()` or `px.choropleth_mapbox()` that shows a geographic or relational pattern in your Taiwan dataset.
3. Add at least one annotation to one chart that highlights a policy-relevant threshold or notable event.
4. Configure hover labels so they show meaningful values (not raw column names).
5. Write two sentences below each chart in Streamlit (`st.caption()` or `st.write()`) summarizing what the chart shows.

Push the updated app to GitHub and redeploy to Streamlit Cloud. Submit the updated Streamlit Cloud URL before Week 14.

---

## Resources

- [Plotly Express documentation](https://plotly.com/python/plotly-express/)
- [Plotly choropleth maps guide](https://plotly.com/python/mapbox-county-choropleth/)
- [Streamlit st.plotly_chart reference](https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart)
- [Altair documentation](https://altair-viz.github.io/)
- [Altair in Streamlit](https://docs.streamlit.io/develop/api-reference/charts/st.altair_chart)
- [Fundamentals of Data Visualization (Wilke, open access)](https://clauswilke.com/dataviz/)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 14 | Add an AI feature — call the Claude API from inside your Streamlit app |
| 15 | Final project workshop — peer code review and presentation rehearsal |
| 16 | **Final milestone:** Live app presentation and symposium |
