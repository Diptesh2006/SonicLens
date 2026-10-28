# Architecture

The Next.js client fetches typed dataset observations from FastAPI, plots them with Recharts and requests deterministic summaries/plans from `/api/analysis`. The backend owns numeric facts and event evidence. The browser maps selected observations to Web Audio oscillator pitch and schedules the chart cursor from the same sequence. Voice providers are deliberately not substituted with browser speech APIs. Current API data lives in memory and resets on server restart; SQLite/session persistence is a planned milestone.
