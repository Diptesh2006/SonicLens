# SonicLens progress

## Current checkpoint — 29 October 2026

The product direction is now voice led time series investigation. The central journey is spoken goal → constrained deterministic analysis → persisted evidence linked to a presentation scene → spoken narration. Energy is a demonstration domain, API telemetry is a second domain, and sonification is an optional Audio Lab.

Implemented in this slice: session goals and presentation states, validated scene and evidence references, persisted scene history and restore route, investigation steps, scene driven area/bar chart presentation, voice interruption during narration, and stale response protection. The input and narration paths use the existing Gnani Prisma/Timbre adapters when configured.

Verification on the D: build copy: API suite was extended for scene persistence/restoration; 28 tests passed before the new assertions, and the final rerun is pending. Frontend TypeScript typecheck and optimized Next.js production build passed. A physical microphone and speaker check remains a user device check. Live provider calls from earlier work are documented; this turn did not re-exercise them.

## Resumable next steps

1. Finish the final API test rerun and verify scene history plus interruption in a browser.
2. Complete architecture/API/demo/test evidence docs and update all DOD status claims to match this implementation.
3. Sync reviewed source and documentation changes to the original checkout, commit with conventional format and push `main`.
4. Keep physical microphone, audible output and repeatable recording as open manual checks unless performed on the user's device.
