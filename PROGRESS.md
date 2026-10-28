# SonicLens progress

## Current checkpoint

Phase 1 data vertical slice: first implementation committed; backend tests and web typecheck pass. Web production build remains blocked by an incomplete installed `caniuse-lite` package in the OneDrive workspace. Browser verification is still outstanding.

## Implemented in working tree

- FastAPI health, dataset listing/detail, analysis and CSV import routes.
- Seeded synthetic energy (168 hourly samples with a known spike) and telemetry (144 samples with correlated latency/error spike).
- Summary, median/MAD outliers, abrupt changes, evidence rows and configurable energy tariff estimate.
- SQLite dataset/session persistence; bounded local query intent; aligned two-period comparison result.
- Session focus validation, deterministic demo reset, strict CSV timestamp/value validation.
- Intent clarification controls, metric aliases, tariff-grounded cost routing, and explicit refusal to infer causes from measurements alone.
- Next.js workspace with backend chart, metric/mode selection, range control, actual Web Audio sonification, playback cursor/rate/volume and CSV upload.
- PRD and user supplied master prompt copied to repository.

## Tests and remaining failures

- Backend: `python -m pytest test_api.py -q` → 19 passed (CSV safety, comparison, sessions/followups, intent clarification, metric/cost routing, voice adapters mocked).
- Frontend `npm run typecheck` → pass.
- Frontend `npm run build` → failed because installed `caniuse-lite/dist/lib/statuses` is missing. `npm install` exits successfully but leaves this package incomplete here.
- No browser visual or audible verification has been performed: Next client compilation succeeds but a later runtime/build worker exits parsing JSON metadata, before binding localhost:3000.
- Gnani server adapters and microphone UI exist; provider tests are mocked. Live Prisma/Timbre remains blocked by absent credentials.
- Gnani integration is not implemented or verified. Voice button is visibly disabled.
- SQLite persistence, sessions/follow-up agent, robust comparisons, production polish and browser verification remain.

## Next actions

1. Restore complete npm package installation in this workspace or a non-synced checkout and rerun build.
2. Start both processes and inspect browser interaction and sound.
3. Record evidence and fix any behavior issues.
4. Continue with browser startup/visual checks, robust analysis semantics and user-facing usability; live Gnani verification remains credential-dependent.
