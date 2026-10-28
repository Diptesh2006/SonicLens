# SonicLens

SonicLens explores time-series datasets with computed evidence, an interactive chart and browser-generated sound. Seed data is synthetic. The current first slice supports energy and API telemetry demos plus CSV import.

## Requirements

- Python 3.11 or newer
- Node.js 20 or newer and npm

## Run locally

Terminal 1:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Terminal 2:

```powershell
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000. The API and OpenAPI page are at http://localhost:8000 and http://localhost:8000/docs.

## Verification

Run API tests with `cd apps/api; python -m pytest -q`. Run web checks with `cd apps/web; npm run typecheck` and `npm run build`.

## Current capabilities and limits

- Synthetic seven-day interval energy and 24-hour API telemetry fixtures.
- Backend mean, range, robust outlier and abrupt-change analysis; energy cost uses the explicitly labeled ₹8/kWh demo tariff (editable through the API).
- CSV import accepts up to 10 MB and 50,000 rows, with an explicit time column and numeric metric.
- Trend/anomaly/comparison playback maps values to local oscillator tones after clicking Play. Browser autoplay restrictions are respected by the user gesture.
- Gnani Prisma/Timbre, SQLite persistence, conversational sessions, fully aligned period comparison, and browser E2E are not implemented yet. The microphone control is disabled and voice is labeled unconfigured.

See [PRD.md](PRD.md), [GOALS.md](GOALS.md), and [PROGRESS.md](PROGRESS.md) for scope and current status.
