# SonicLens goals

Statuses: `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED_EXTERNAL`.

| ID | Acceptance criterion | Status | Verification / evidence |
|---|---|---|---|
| DOD-01 | Documented local frontend and API startup | PASS | README startup commands used to launch API on 8000 and production web app on 3000 |
| DOD-02 | Bounded CSV import, UTC normalization, ordering, duplicate/non-finite validation, missing-value and editable unit handling | PASS | 28 API tests pass, including CSV ordering, duplicate timestamps, Infinity, missing rows, and persistent unit edits; limits 10 MB/50k rows |
| DOD-03 | Synthetic energy and telemetry datasets | PASS | Browser loaded 168 energy and 144 telemetry observations after deterministic reset |
| DOD-04 | Chart shows backend observations and selected metric/range | PASS | Browser range changed energy coverage 168→48; dataset switch showed telemetry latency and its range-specific values |
| DOD-05 | Summary, local peaks, outlier, abrupt-change and aligned period comparison | PASS | API tests verify computed values; browser comparison returned 84 aligned time-of-day pairs |
| DOD-06 | Energy cost uses labeled tariff and confirmed interval kWh; never treats kW as kWh | PASS | API tests cover seed tariff, explicit CSV kWh confirmation and no estimate for kW power samples |
| DOD-07 | Browser generates data-mapped trend audio | IN_PROGRESS | Web Audio is gesture-started and cursor advances; audio device output has not been independently heard |
| DOD-08 | Anomaly mode focuses detected intervals | PASS | Browser selected anomaly mode; persisted analysis returned event focus; playback controls operated |
| DOD-09 | Comparison mode uses aligned series observations and reports differences | PASS | 84 aligned energy pairs verified in browser; comparison playback cursor advances over paired indices and uses signed difference pitch mapping |
| DOD-10 | Playback controls, focus range, rate, volume | PASS | Browser verified play, pause, resume, stop and range; speed set to 2×, volume set to 0 and cursor still advanced silently |
| DOD-11 | Chart cursor tracks scheduled notes | PASS | Browser timeline timestamp advanced during playback in trend/comparison flows |
| DOD-12 | Constrained natural-language intent routes analysis | PASS | 28 API tests cover English/Hinglish intents, aliases, cost and clarification |
| DOD-13 | Follow-up context resolution | PASS | API tests verify previous-period alignment, replay speed, persisted turns and unsupported-cause refusal |
| DOD-14 | Results have inspectable, persistent evidence IDs and source samples | PASS | API verifies storage/retrieval; browser expanded table with 168 source rows matching first/last persisted UTC timestamps |
| DOD-15 | Authentic server-side Gnani Prisma adapter | IN_PROGRESS | Official streaming adapter and mocked contract tests implemented; authenticated live request not run |
| DOD-16 | Authentic server-side Gnani Timbre adapter | IN_PROGRESS | Official REST/WAV adapter and mocked tests implemented; authenticated live request not run |
| DOD-17 | Live Gnani microphone-to-spoken-answer journey | BLOCKED_EXTERNAL | Local `.env` is ready but `GNANI_API_KEY` is blank; route surfaces 503 and mic is disabled |
| DOD-18 | Hindi-English spoken request verified | BLOCKED_EXTERNAL | Requires configured key, account-entitled model, and live microphone run |
| DOD-19 | Actionable upload and API errors | PASS | 28 API tests cover invalid schema, duplicates, non-finite values, invalid metrics/ranges and voice errors |
| DOD-20 | Synthetic data and local audio labels are honest | PASS | Browser confirmed synthetic fixture labels, unconfigured voice label and no synthetic badge on CSV uploads by implementation |
| DOD-21 | Responsive desktop and mobile layout | PASS | Browser at 390×844 showed key controls, evidence table and chart; document scroll width remained 390 px; screenshot visually reviewed |
| DOD-22 | Server-side keys, bounded uploads, constrained operations | PASS | API tests confirm missing credentials and limits; voice keys are read server-side and operation routing is bounded |
| DOD-23 | Backend tests, frontend typecheck and production build | PASS | `python -m pytest test_api.py -q` 28 passed; `npm run typecheck` and `npm run build` exit 0 |
| DOD-24 | Browser end-to-end seeded exploration | PASS | Production browser loaded app; trend/anomaly/comparison, range, playback and telemetry switch checked; final console had 0 errors |
| DOD-25 | Repeatable demo recording flow | IN_PROGRESS | Resettable browser walkthrough works; audio capture recording was not produced in this environment |
| DOD-26 | Setup, architecture, API, voice, audio and demo docs | PASS | README, architecture, API, Gnani setup, sonification, demo and sound evaluation docs reviewed and updated against current implementation |
| DOD-27 | Energy and telemetry share engine | PASS | Browser switched energy→telemetry and analysis updated to the telemetry metric without errors |
| DOD-28 | Blinded sound-value evaluation exists without efficacy claims | PASS | `docs/SOUND_EVALUATION.md` specifies randomized clips, blinded answer key and cautious reporting; no results are claimed |
