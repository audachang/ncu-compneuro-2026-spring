# Cognitive Aging Dashboard — Week 11 Demo

Streamlit dashboard for a synthetic lifespan cognitive battery (n=400, ages 20–80).

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Files

```
app/
├── app.py                 # main Streamlit app
├── generate_dataset.py    # creates data/cognitive_aging_taiwan.csv
├── requirements.txt
└── data/
    └── cognitive_aging_taiwan.csv
```

## Deploy to Streamlit Cloud

1. Push the `app/` contents to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**.
3. Pick the repo, branch, and `app.py`. Click **Deploy**.

Course: NS5116 Programming & AI Applications in Behavioral Science · Spring 2026 · ACL@NCU
