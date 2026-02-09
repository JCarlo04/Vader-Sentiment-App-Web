
# Vader Sentiment App — Instructions

## Overview
A local sentiment-analysis project built around VADER with:
- A Tkinter desktop GUI for quick local analysis and an inline pie visualization.
- A Flask web UI (modern, clean theme) that categorizes submitted texts into Positive / Neutral / Negative and visualizes distribution.
- A small preprocessor to normalize elongated words (e.g. "looove" → "loove") and reduce punctuation bias.

## Basic functions
- Analyze text with VADER (via vaderSentiment) and a lightweight preprocessor.
- Classify each submitted text as `positive`, `neutral`, or `negative`.
- Store recent entries in memory and display them grouped by category.
- Web UI shows a pie chart driven by category counts (so empty categories do not dominate the chart).

## Technical specifications
- Python 3.8+
- Dependencies:
  - vaderSentiment
  - Flask (web UI)
  - Chart.js (client-side via CDN)
- Key files:
  - `src/sentiment.py` — SentimentAnalyzer (preprocessing + VADER calls)
  - `src/app.py` — Tkinter desktop GUI
  - `src/web.py` — Flask web application
  - `src/templates/*` — Jinja2 templates for web UI
  - `src/static/*` — CSS and static assets
  - `Instructions.md` — this file

## Quick start (Windows)
1. Open PowerShell or CMD in project root (vader-sentiment-app).
2. Create & activate a venv (recommended)
   - PowerShell:
     ```
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - CMD:
     ```
     python -m venv .venv
     .\.venv\Scripts\activate.bat
     ```
3. Install dependencies:
   ```
   python -m pip install vaderSentiment flask
   ```
   (Or: `python -m pip install -r requirements.txt` if you add one.)
4. Run the desktop GUI:
   - From project root:
     ```
     python -m src.app
     ```
     or
     ```
     cd src
     python app.py
     ```
5. Run the web app:
   - From project root:
     ```
     python -m src.web
     ```
     Open http://127.0.0.1:5000 in your browser.

## Notes on behavior
- The web pie chart is driven by the counts of entries per category (positive/neutral/negative). Empty categories are excluded from the chart to avoid misleading slices.
- Storage is in-memory. Restarting the web app clears stored texts.

## Suggestions for further work
- Persist storage (SQLite + SQLAlchemy) so entries survive restarts.
- Add authentication / per-user stores.
- Expand preprocessing: emoji handling, improved token normalization, and custom lexicon entries.
- Add unit tests (pytest), CI (GitHub Actions), and a `requirements.txt`.
- Dockerize the web app for deployment.
- Add export/import (CSV/JSON) for stored entries.

## Contributing
- Fork, make a feature branch, and open a PR.
- Keep changes focused; update this file when adding notable features.

## License
- Add a LICENSE file (e.g., MIT) if you want to publish under an open-

## Preview Image of the Web Client

![Vader Client Image](https://github.com/JCarlo04/Vader-Sentiment-App-Web/blob/main/preview.png)

