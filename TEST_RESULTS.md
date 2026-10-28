# Test results

Results recorded 2026-10-28 (local Windows/OneDrive checkout):

- `python -m pytest test_api.py -q` (working directory `apps/api`): **PASS**, 4 passed.
- `npm install --no-audit --no-fund` (working directory `apps/web`): **PASS**, exit 0.
- `npm run typecheck` (working directory `apps/web`): **PASS**, exit 0 after correcting a narrowed dataset reference.
- `npm run build` (working directory `apps/web`): **FAIL / environment dependency corruption**. Next.js cannot resolve `caniuse-lite/dist/lib/statuses`; the installed package contains `dist/unpacker` but no `dist/lib`. Reinstall/force reinstall did not restore the missing package files in this OneDrive workspace.
- `git diff --check`: **PASS** before first commit.

Not yet run: browser/manual audio, responsive UI, API process smoke, or browser E2E. Do not infer results from source inspection.

