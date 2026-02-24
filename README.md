# NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用 
## The Applications of Computer Hardware and Programming Languages in Behavioral Experiments and Big-Data — Spring 2026

> **Teacher:** Erik Chang (張智宏) | **Code:** NS5116 | **Credits:** 3
> **Time:** Thursdays 9:00AM ~ 12:00PM | **Room:** TBA | **Term:** Spring 2026

## Goal of the Course
本課程的目標在於將研究生從程式設計的門外漢轉化為具備「AI 協作開發」能力的跨領域研究者。透過從底層 Python 語法到高階 AI 代理工具的學習，本課程指出了現代行為科學研究者的必備技能：不僅要能設計嚴謹的認知實驗，更要具備處理大數據並將其轉化為互動式網頁應用的能力。最終，學生將能靈活運用 AI 工具解決研究中的技術瓶頸，並在行為科學與大數據分析的交界處實現創新。

## Course Overview
這門課程 NS5116 電腦硬體與程式語言在行為科學實驗與大數據分析之應用 是一門為研究生量身打造的實戰型編碼課。課程設計分為兩大階段：前半段聚焦於 「手動 Python」 (Manual Python)，旨在幫助零基礎學生建立紮實的程式邏輯與數據處理能力，並透過 PsychoPy 實作心理學實驗，最終部署至 Pavlovia 雲端平台；後半段則進入 「氛圍編碼與代理人編碼」 (Vibe Coding & Agentic Programming)，教導學生利用 AI 輔助開發工具（如 Claude Code）快速構建功能完整的 Streamlit 網頁應用，並結合 台灣政府開放資料 API 進行大數據敘事。

A 16-week practical coding course for graduate students. No prior programming experience required.

- **Part 1 (Weeks 1–8) — Manual Python:** Build programming fundamentals from scratch.
  **Milestone:** Deploy a working online cognitive experiment to Pavlovia.
- **Part 2 (Weeks 9–16) — Vibe Coding & Agentic Programming:** Use AI coding tools (Claude Code) to build real applications.
  **Milestone:** Present a live web app using Taiwan government open data.

---

## Weekly Schedule

### Part 1: Manual Python (Weeks 1–8)

| Week | Topic | Tools |
|------|-------|-------|
| [01](week-01-python_setup_and_basic_syntax/) | Environment setup, variables, types, operators | Anaconda, VS Code, Jupyter |
| [02](week-02-control_flow_and_functions/) | if/else, for/while loops, functions, scope, debugging | Python |
| [03](week-03-data_structures_and_file_io/) | Lists, dicts, tuples, sets; CSV & text file I/O | Python |
| [04](week-04-numpy_and_data_manipulation/) | NumPy arrays, indexing, vectorized operations | NumPy |
| [05](week-05-data_visualization_with_matplotlib/) | Line/scatter/bar/histogram plots, subplots, annotations | Matplotlib |
| [06](week-06-psychopy_basics_stimuli_and_windows/) | PsychoPy install, Window, visual stimuli, clocks, input | PsychoPy |
| [07](week-07-psychopy_experiment_design/) | Event loop, trial structure, response recording, data saving | PsychoPy, Pavlovia |
| **[08](week-08-midterm_online_experiment_on_pavlovia/)** | **MILESTONE: Deploy cognitive experiment to Pavlovia** | PsychoPy, Pavlovia |

### Part 2: Vibe Coding & Agentic Programming (Weeks 9–16)

| Week | Topic | Tools |
|------|-------|-------|
| [09](week-09-intro_to_vibe_coding_and_claude_code/) | Vibe/agentic coding concepts; Claude Code CLI setup; prompting | Claude Code |
| [10](week-10-agentic_workflows_and_github/) | Multi-step task delegation, git commits, GitHub Actions | Claude Code, GitHub |
| [11](week-11-web_app_development_with_streamlit/) | Streamlit app; layout, widgets, charts; deploy to Streamlit Cloud | Streamlit |
| [12](week-12-open_data_apis_and_data_engineering/) | Taiwan gov open data portal (data.gov.tw), API calls, data cleaning | pandas, requests |
| [13](week-13-interactive_dashboards_and_storytelling/) | Interactive charts, narrative data storytelling | Plotly, Altair |
| [14](week-14-ai_features_with_claude_api/) | Anthropic SDK; add AI features; responsible AI | Anthropic SDK |
| [15](week-15-final_project_workshop/) | Peer code review; polish UI/UX; documentation; rehearsal | Claude Code |
| **[16](week-16-final_project_presentation/)** | **MILESTONE: Present online app using Taiwan open data** | All |

---

## Grading

| Component | Weight |
|-----------|--------|
| Weekly assignments (Weeks 1–7, 9–14) | 30% |
| Midterm project — Pavlovia experiment (Week 8) | 30% |
| Final project — Taiwan open data web app (Week 16) | 35% |
| Participation & peer review | 5% |

## Prerequisites

- Basic computer skills; no prior programming experience required
- Bring a laptop to every class

## Accounts to Create Before Class

| Service | Purpose | Cost |
|---------|---------|------|
| [GitHub](https://github.com/) | Version control | Free |
| [Pavlovia](https://pavlovia.org/) | Online experiment hosting | Free for students |
| [Streamlit Cloud](https://streamlit.io/cloud) | Web app hosting | Free |

## Repository Structure

```
week-NN-topic-name/
├── README.md              ← Week overview, objectives, assignment
└── week-NN-starter.ipynb  ← Starter notebook to fill in
```

## License

Code: [MIT License](LICENSE) | Materials: [CC BY 4.0](LICENSE-DOCS)
