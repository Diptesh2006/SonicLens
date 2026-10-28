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
- `git diff --check`: **PASS** before first commit.

Not yet run: browser/manual audio, responsive UI, API process smoke, or browser E2E. Do not infer results from source inspection.

