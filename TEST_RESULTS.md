# Test results

Results recorded 2026-10-28 (local Windows/OneDrive checkout):

- `python -m pytest test_api.py -q` (working directory `apps/api`): **PASS**, 4 passed.
- Latest `python -m pytest test_api.py -q`: **PASS**, 6 passed, covering aligned comparison and SQLite session/query persistence.
- Latest `python -m pytest test_api.py -q`: **PASS**, 10 passed, including validated focus bounds, deterministic demo reset, equal-offset comparison evidence, timestamp sorting, duplicate timestamp rejection and Infinity validation.
- `npm install --no-audit --no-fund` (working directory `apps/web`): **PASS**, exit 0.
- `npm run typecheck` (working directory `apps/web`): **PASS**, exit 0 after correcting a narrowed dataset reference.
- `npm run build` (working directory `apps/web`): **FAIL / environment dependency corruption**. Next.js cannot resolve `caniuse-lite/dist/lib/statuses`; the installed package contains `dist/unpacker` but no `dist/lib`. Reinstall/force reinstall did not restore the missing package files in this OneDrive workspace.
- Latest `npm run typecheck` after session/query UI wiring: **PASS**, exit 0.
- Latest backend suite: `python -m pytest test_api.py -q`: **PASS**, 14 passed, including mocked Prisma/Timbre provider-flow and audio validation.
- Latest `npm run typecheck`: **PASS**, exit 0 after microphone capture and provider response UI.
- Latest `npm run build`: Next compiled successfully, then the build worker exited with `SyntaxError: Bad escaped character in JSON`; `npm run dev` exits with the same error before binding port 3000. All installed `package.json` files were checked and parse successfully; issue is in the synced runtime/cache metadata. Playwright CLI navigation to localhost consequently returned `ERR_CONNECTION_REFUSED`.
- Latest backend suite after intent clarification and metric/cost/causal routing: `python -m pytest test_api.py -q`: **PASS**, 19 passed.
- Latest `npm run typecheck` after clarification controls: **PASS**, exit 0.
- Latest backend suite after per-metric units, missing-observation handling, and valid plan-event filtering: `python -m pytest test_api.py -q`: **PASS**, 21 passed.
- Latest `npm run typecheck` after pause/resume controls and unit editor: **PASS**, exit 0.
- Latest backend suite: `python -m pytest test_api.py -q`: **PASS**, 23 passed, including explicit CSV sampling-kind semantics and kW cost prohibition.
- Latest `npm run typecheck` after unit/sampling editor: **PASS**, exit 0.
- Latest backend suite: `python -m pytest test_api.py -q`: **PASS**, 26 passed, including shifted-window time-of-day alignment and pair evidence.
- Latest `npm run typecheck` after evidence metadata and voice status UI: **PASS**, exit 0.
- Latest backend suite: `python -m pytest test_api.py -q`: **PASS**, 28 passed, including stored evidence reload and the 12-second PCM limit.
- Latest `npm run typecheck` after evidence reload control: **PASS**, exit 0.
- `git diff --check`: **PASS** before first commit.

Not yet run: browser/manual audio, responsive UI, API process smoke, or browser E2E. Do not infer results from source inspection.

## Production and browser verification (2026-10-28)

- `python -m pytest test_api.py -q` (working directory `apps/api`): **PASS**, 28 passed in 3.67s.
- `npm run typecheck` (working directory `apps/web`): **PASS**, exit 0 after evidence table and chart description changes.
- `npm run build` (working directory `apps/web`): **PASS**, Next.js 15.5.28 production build, including `/`, `/_not-found`, and `/icon.svg`.
- API smoke: launched Uvicorn from this checkout at `http://localhost:8000`; `POST /api/demo/reset` succeeds and restores energy + telemetry fixtures.
- Production browser: launched via `npm run start` from this checkout at `http://localhost:3000`; page title and data load verified.
- Browser anomaly flow: switched analysis to anomaly; backend evidence ID persisted and returned; Playwright clicked Play, Pause, Resume and Stop.
- Browser comparison flow: selected comparison, verified 84 aligned pairs and signed delta evidence; playback timeline cursor advanced during paired playback.
- Browser evidence: expanded the source table and saw 168 rows; first/last UTC timestamps matched the stored analysis response.
- Browser range/domain: changing range updated coverage and computed chart description; switching to telemetry selected `latency_ms`, updated the chart description, showed no error banner, and produced no console errors after the atomic metric-selection fix.
- Browser console after rebuilding/restarting the app from the actual checkout: **0 errors, 0 warnings**. Earlier 404 output came from the stale temporary probe server; it disappeared once the verified checkout server was used.
- Still unverified: direct browser CSV upload and unit editor flow, narrow/mobile layout review, physical speaker/headphone audibility, and authenticated live Gnani calls. The latter remain credential-dependent; no live call is claimed.
- Follow-up production checks after CSV selection and audio safeguards: `npm run typecheck` and `npm run build` both **PASS**; backend suite still **28 passed**.
- Direct CSV browser flow: imported a 3-row CSV with one blank value; UI showed `Missing`; after setting unit `kWh` and sampling kind `interval_energy`, energy estimate became ₹28.80 for the two observed readings at ₹8/kWh. Upload selected metric `usage` without errors.
- Responsive browser check at 390×844: heading, chart, player and source table visible; `document.documentElement.scrollWidth` was 390, matching viewport width. Screenshot visually reviewed.
- Speed/volume browser check: selected 2× and zero volume, started playback, verified cursor advanced, then stopped; volume zero short-circuits tone scheduling.
- Final production browser after audio safeguard changes: deterministic reset, anomaly selection, cursor movement, pause/resume/stop succeeded; console **0 errors, 0 warnings**.
- Current unverified items: listening on a physical output device, authenticated live Gnani, and producing a recorded demo artifact. No results are claimed for these.

