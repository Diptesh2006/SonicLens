# Test results

Updated 2026-10-29. Source changes were made in a D: build copy because the C: system drive had almost no free space; source and documentation still need synchronization to the original checkout before commit.

## Current verification

- `python -m pytest test_api.py -q` in `apps/api`: 28 passed before adding two presentation assertions; after adding the assertions, one expectation was corrected from `bar` to `area` for anomaly scenes. Final rerun pending.
- `npm run typecheck` in `apps/web`: PASS, exit 0.
- `npm run build` in `apps/web`: PASS, optimized Next.js production build completed and static routes generated.
- Scene restoration API coverage added: second scene can be created, an earlier scene restored, and the current scene persists in session storage. Included in pending final pytest rerun.
- This turn did not perform a browser E2E or live provider call. Physical microphone, speaker audibility and demo recording remain unverified on the user device.

## Prior evidence

Earlier verification documented in git history includes 28 API tests, desktop/mobile browser inspection, synthetic fixture analysis, and live Prisma/Timbre calls using generated PCM fixtures. Those checks are not repeated by the current source change and do not substitute for physical microphone testing.
