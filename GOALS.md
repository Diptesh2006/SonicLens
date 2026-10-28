# SonicLens goals

Statuses: `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED_EXTERNAL`.

| ID | Acceptance criterion | Status | Verification / evidence |
|---|---|---|---|
| DOD-01 | Local documented frontend/API setup | PASS | Existing README commands; fresh setup not re-run this turn |
| DOD-02 | Bounded CSV import and explicit units | PASS | Existing 28 API tests cover limits, timezone, duplicate/non-finite values and missing rows |
| DOD-03 | Synthetic energy and telemetry datasets | PASS | Existing API/browser verification; 168 and 144 observations |
| DOD-04 | Charts show backend values and ranges | IN_PROGRESS | Scene-driven area/bar renderer typechecked and production-built; browser scene behavior not rechecked this turn |
| DOD-05 | Deterministic summary/anomaly/comparison calculations | PASS | Existing API suite; energy and telemetry share analysis route |
| DOD-06 | Explicit interval-kWh cost semantics | PASS | Existing API tests cover confirmed units and kW exclusion |
| DOD-07–11 | Supplementary sonification and controls | IN_PROGRESS | Existing browser evidence; Audio Lab moved into disclosure, not rechecked in browser |
| DOD-12 | Voice goal routes to bounded analysis and presentation | IN_PROGRESS | New API assertions added for goal, four executed steps, scene, evidence ID and chart mode; final pytest pending |
| DOD-13 | Dataset-aware follow-up context | IN_PROGRESS | Prior tests cover comparison and playback follow ups; new scene history not browser verified |
| DOD-14 | Spoken answers link to persistent inspectable evidence | IN_PROGRESS | Scene evidence points to saved analysis and API restore coverage added; final suite pending |
| DOD-15–16 | Authenticated Prisma and Timbre adapters | PASS | Prior real provider requests recorded in previous evidence; not re-exercised this turn |
| DOD-17 | Physical mic → Prisma → analysis → Timbre → audible reply | IN_PROGRESS | Generated audio fixture proved provider chain earlier; physical user microphone/speaker still unverified |
| DOD-18 | Hindi-English spoken request | PASS (fixture only) | Prior generated code-mixed audio fixture transcribed and routed; real speaker utterance remains unverified |
| DOD-19 | Voice interruption and stale-result safety | IN_PROGRESS | Mic remains enabled during playback, pauses narration, generation guards stale frontend responses; browser check pending and provider in-flight work is not cancellable |
| DOD-20 | Honest synthetic/provenance labels | IN_PROGRESS | Copy generalized and seeded data still marked synthetic; browser review pending |
| DOD-21 | Responsive interface | IN_PROGRESS | Previous viewport checks predate this UI change; repeat browser review pending |
| DOD-22 | Server-only secrets and bounded operations | PASS | Existing API validation and environment handling; no secrets copied into source |
| DOD-23 | API suite, frontend typecheck and production build | IN_PROGRESS | Typecheck/build pass on D: copy; final API rerun pending |
| DOD-24 | Browser voice → scene → follow-up → restore journey | IN_PROGRESS | Not exercised in browser this turn |
| DOD-25 | Repeatable voice-led demo | IN_PROGRESS | Walkthrough updated; physical recording not captured |
| DOD-26 | Product, presentation, API and demo documentation | IN_PROGRESS | README, PRD, architecture, API, demo, progress, decisions and test evidence updated; final review pending |
| DOD-27 | Shared engine for energy, telemetry and CSV | PASS | Existing API contract and UI path; product copy now general |
| DOD-28 | Blinded listening study without efficacy claims | PASS | Existing protocol retained; no study outcome claimed |

## Current slice acceptance

- [x] Scene schema validates dataset, metric and saved analysis linkage.
- [x] Session persists goal, state, steps, current scene and up to 20 scenes.
- [x] Query response supplies the scene, history and executed investigation steps.
- [x] Scene restore validates evidence and updates active metric/mode/range.
- [x] Frontend maps area/bar scene to the live chart and renders step/history navigation.
- [x] Voice capture can interrupt local narration; generation tokens reject stale browser results.
- [ ] Final API suite, browser inspection, original checkout sync, conventional commit and push.
