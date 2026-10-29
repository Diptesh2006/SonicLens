# SonicLens

SonicLens is a voice led time series analyst. Speak an analytical goal and it investigates a selected dataset, updates a presentation scene, shows supporting readings, and narrates the grounded result. Energy usage and service telemetry are demonstration datasets that share the same analysis engine; CSV import lets you explore timestamped data.

## Run locally

Requirements: Python 3.11+, Node.js 20+ and npm. Use two PowerShell terminals from the repository root.

Add your Gnani key to the ignored root `.env` as `GNANI_API_KEY=...` to enable server side Prisma transcription and Timbre narration. The API reads it on startup; never commit it. A safe template is in `.env.example`. Without the key, supported browsers can use built in speech recognition for spoken questions; typed questions are always available.

API terminal:

```powershell
cd apps/api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Web terminal:

```powershell
cd apps/web
npm ci
npm run dev
```

Open <http://localhost:3000>. API health is <http://localhost:8000/api/health>; interactive API docs are at <http://localhost:8000/docs>.

## Voice led walkthrough

1. Select energy or API telemetry, or import a CSV with timezone aware timestamps and numeric columns.
2. Tap the microphone and ask “Give me an overview”, “Find unusual spikes”, or “Compare with the previous period”. If browser speech recognition is unavailable, type the question in the always visible field.
3. Follow the answer, investigation steps, chart scene and evidence as they update together. Speak again while narration plays to interrupt and redirect it.
4. Restore an earlier scene from scene history. Open **Optional Audio Lab** for supplementary sonification.

When configured, voice uses server side Gnani Prisma and Timbre. Browser speech recognition is a local input fallback and does not produce spoken narration; use Gnani for the full spoken loop. Analysis uses bounded deterministic tools and does not claim causes unsupported by the measurements. Seeded datasets are synthetic. Energy cost requires confirmed interval kWh and a supplied tariff.

## Verify

```powershell
cd apps/api
python -m pytest test_api.py -q
cd ../web
npm run typecheck
npm run build
```

Technical reference: [API](docs/API.md), [architecture](docs/ARCHITECTURE.md), [voice setup](docs/GNANI_SETUP.md), [presentation engine](docs/PRESENTATION_ENGINE.md) and [demo guide](docs/DEMO.md).
