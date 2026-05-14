# Week 15: Final Project Workshop

> **Course:** NS5116 Programming & AI Applications in Behavioral Science — Spring 2026
> **Week:** 15 of 16 | **Date:** 2026-06-04 | **Room:** TBA

---

## Overview

This is a studio/workshop week. There is no lecture. The full class period is dedicated to finalizing your project in a structured sequence: peer code review, UI polish based on feedback, README writing, and a presentation rehearsal. You will leave class with a deployment-ready application and a rehearsed 10-minute talk.

---

## Learning Objectives

By the end of this week you will be able to:

1. Conduct a structured peer code review using Claude Code
2. Give and receive specific, actionable feedback on a Streamlit application
3. Apply at least three UI/UX improvements based on reviewer feedback
4. Write a project README that a new user can follow without help
5. Rehearse a 10-minute live demo presentation and receive timing feedback
6. Confirm your app is deployed on Streamlit Cloud and loads without errors

---

## Workshop Schedule

| Time | Activity |
|------|---------|
| 0:00–0:20 | Final deployment check — confirm app is live |
| 0:20–1:00 | Peer code review (pairs, 20 min each direction) |
| 1:00–1:20 | Apply reviewer feedback |
| 1:20–1:40 | README writing sprint |
| 1:40–2:10 | Presentation rehearsals (5 min per person) |
| 2:10–2:30 | Buffer: final fixes, questions |

---

## Step 1: Final Deployment Check (20 min)

Before peer review begins, confirm:

```
Deployment Checklist
--------------------
[ ] App loads at the Streamlit Cloud URL in an incognito browser window
[ ] All charts render without errors
[ ] All widgets respond correctly
[ ] Chat / AI feature works (if your API key is in st.secrets)
[ ] No "ModuleNotFoundError" — requirements.txt is complete
[ ] App loads in under 15 seconds (check @st.cache_data is in place)
[ ] No API keys, passwords, or personal data visible in the app
[ ] GitHub repository is public
```

If the app fails the deployment check, spend this time fixing it before peer review starts.

---

## Step 2: Peer Code Review (40 min)

Work in pairs. Each partner reviews the other's repository and app for 20 minutes, then you swap.

**How to run a Claude Code review:**

```bash
# In your partner's cloned repository
claude

> Review this Streamlit project as a senior developer.
  Check: code quality, missing error handling, hardcoded values,
  security issues (API keys), performance (missing cache), and
  any widget or chart that does not work as described in the README.
  List each issue with a suggested fix and an effort estimate (small/medium/large).
```

**Peer Review Checklist**

Use this checklist to structure your feedback. Add written notes in a shared document or as a GitHub Issue.

```
CODE QUALITY
[ ] Functions are short and single-purpose (under ~30 lines each)
[ ] No code duplication — shared logic is in utils/
[ ] No hardcoded file paths, station names, or thresholds
[ ] All imports are used; no unused variables
[ ] No bare except: clauses

DATA & API
[ ] @st.cache_data is applied to every data loading function
[ ] API errors produce an informative error message (not a crash)
[ ] Data cleaning is documented (what does each step fix?)

UI / UX
[ ] Page title and section headers are clear
[ ] Chart axes are labelled with units
[ ] Charts respond correctly to widget selections
[ ] Widgets have sensible default values
[ ] A new user can understand the app without instructions

AI FEATURE
[ ] System prompt clearly defines scope
[ ] Disclaimer is shown near the chat interface
[ ] API key is not visible in source code or git history

SECURITY
[ ] .env is in .gitignore
[ ] secrets.toml is in .gitignore
[ ] No personal participant data is in the repository

PRESENTATION READINESS
[ ] README explains the project, data source, and how to run locally
[ ] requirements.txt is complete
[ ] GitHub repository has a descriptive title and description
```

---

## Step 3: Apply Reviewer Feedback (20 min)

After receiving your review, triage the issues:

1. **Fix immediately (< 5 min):** missing chart labels, hardcoded strings, typos in the README
2. **Fix before Week 16 (tonight):** broken widget logic, missing error handling, cache not applied
3. **Future work:** features the reviewer suggested but that are out of scope for the final presentation

Use Claude Code to apply fixes quickly. Give it the specific issue from the review:

```
> My reviewer noted that the line chart does not update when the user
  changes the station selectbox. The filtered DataFrame is computed
  correctly but is not passed to the chart function. Fix it.
```

---

## Step 4: README Writing Sprint (20 min)

A good project README answers five questions:

1. **What does this app do?** — One or two sentences.
2. **What data does it use?** — Dataset name, source URL, time range, key variables.
3. **What can a user do?** — List the main features (filters, charts, AI chat).
4. **How do I run it locally?** — Step-by-step install and run instructions.
5. **What are the limitations?** — Data freshness, geographic coverage, AI accuracy.

**README template:**

```markdown
# [Project Title]

A Streamlit web app that [one-sentence description].

**Live app:** [Streamlit Cloud URL]

## Data source

- Dataset: [name]
- Provider: [e.g., Taiwan EPA, data.gov.tw]
- URL: [link]
- Coverage: [e.g., 2018–2024, 76 monitoring stations]

## Features

- Filter by county and date range
- Interactive PM2.5 trend chart by station
- County-level choropleth map
- AI Q&A assistant for health guidance

## Run locally

```bash
git clone https://github.com/your-username/your-repo
cd your-repo
pip install -r requirements.txt

# Add your API key
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

streamlit run app.py
```

## Limitations

- Data updated daily; readings from the last 24 hours may be incomplete.
- AI responses are for general information only and do not constitute medical advice.
```

---

## Step 5: Presentation Rehearsal (30 min)

Each student rehearses their Week 16 presentation. You have **5 minutes** for your rehearsal slot. The instructor will time you and give one piece of feedback.

**Presentation structure for Week 16 (8 min demo + 2 min Q&A):**

| Section | Time | What to cover |
|---------|------|--------------|
| Problem and data | 1.5 min | What question does your app answer? What data does it use? |
| Live demo | 4.5 min | Show the app working: filter, chart, map, AI feature |
| Key finding | 1 min | What did you discover from the data? |
| What you learned | 1 min | What was the hardest part to build? What would you add next? |
| Q&A | 2 min | Answer audience questions |

**Rehearsal feedback form** (fill in for your partner):

```
Timing:        [over / on time / under]
Problem clear: [yes / no — what was unclear?]
Demo smooth:   [yes / no — what broke or was confusing?]
Finding clear: [yes / no — what was the main result?]
One suggestion: [specific and actionable]
```

---

## Before Week 16 — Final Submission Checklist

Complete these before the day of presentations:

```
[ ] App deployed and publicly accessible on Streamlit Cloud
[ ] All charts render without error
[ ] AI chat feature works with st.secrets API key
[ ] GitHub repository is public
[ ] README is complete (title, data source, features, run instructions)
[ ] requirements.txt is up to date (pip freeze > requirements.txt)
[ ] .env and secrets.toml are in .gitignore and NOT in the repository
[ ] Presentation rehearsed and timed at 8 minutes
[ ] Laptop charged and connected to the classroom display
[ ] Streamlit Cloud URL ready to share (no login required)
```

---

## Tools This Week

| Tool | Purpose |
|------|---------|
| Claude Code CLI | Automated code review and targeted fixes |
| GitHub Issues | Track feedback items from peer review |
| Streamlit Cloud | Confirm deployment is stable |
| `pip freeze` | Generate a complete `requirements.txt` |

---

## Resources

- [Streamlit deployment checklist](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app)
- [Writing a good README (makeareadme.com)](https://www.makeareadme.com/)
- [Streamlit performance tips](https://docs.streamlit.io/develop/concepts/architecture/caching)
- [GitHub Issues — tracking bugs and feedback](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues)

---

## What Comes Next

| Week | Topic |
|------|-------|
| 16 | **Final milestone:** 10-minute live app presentation — symposium day |
