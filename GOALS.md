# SonicLens goals

Statuses: `NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `BLOCKED_EXTERNAL`.

| ID | Acceptance criterion | Status | Verification / evidence |
|---|---|---|---|
| DOD-01 | Documented local frontend and API startup | IN_PROGRESS | README commands exist; processes not yet run together |
| DOD-02 | Bounded valid/invalid CSV import | PASS | `python -m pytest test_api.py -q`: valid/import and actionable invalid CSV tests passed; size cap implemented |
| DOD-03 | Synthetic energy and telemetry datasets | PASS | `python -m pytest test_api.py -q`: expected seeded IDs and health count passed |
| DOD-04 | Chart shows backend observations and selected metric/range | IN_PROGRESS | Browser verification pending |
| DOD-05 | Summary, outlier, abrupt-change analysis | IN_PROGRESS | API tests pending execution |
| DOD-06 | Energy cost uses labeled user tariff and interval kWh | IN_PROGRESS | API test pending execution |
| DOD-07 | Browser generates data-mapped trend audio | IN_PROGRESS | Manual audio check pending |
| DOD-08 | Anomaly mode focuses detected intervals | IN_PROGRESS | API and browser checks pending |
| DOD-09 | Comparison mode uses aligned series observations | NOT_STARTED | — |
| DOD-10 | Playback controls, focus range, rate, volume | IN_PROGRESS | Browser verification pending |
| DOD-11 | Chart cursor tracks scheduled notes | IN_PROGRESS | Browser verification pending |
| DOD-12 | Constrained natural-language intent routes analysis | IN_PROGRESS | Deterministic keyword mapping only; tests pending |
| DOD-13 | Follow-up context resolution | NOT_STARTED | — |
| DOD-14 | Results have inspectable evidence IDs and source samples | IN_PROGRESS | API response implemented; test pending |
| DOD-15 | Authentic server-side Gnani Prisma adapter | NOT_STARTED | Credentials/configuration not inspected beyond environment names |
| DOD-16 | Authentic server-side Gnani Timbre adapter | NOT_STARTED | Credentials/configuration not inspected beyond environment names |
| DOD-17 | Live Gnani microphone-to-spoken-answer journey | BLOCKED_EXTERNAL | No Gnani credentials found in process environment; recheck at integration phase |
| DOD-18 | Hindi-English spoken request verified | NOT_STARTED | Depends on configured live provider/model |
| DOD-19 | Actionable upload and API errors | IN_PROGRESS | Automated checks pending |
| DOD-20 | Synthetic data and local audio labels are honest | IN_PROGRESS | UI labels; visual review pending |
| DOD-21 | Responsive desktop and mobile layout | IN_PROGRESS | CSS added; browser check pending |
| DOD-22 | Server-side keys, bounded uploads, constrained operations | IN_PROGRESS | No voice keys in frontend; upload cap implemented; audit pending |
| DOD-23 | Backend tests, frontend typecheck and production build | FAIL | pytest 4 passed; `npm run typecheck` passed; `npm run build` failed on missing installed `caniuse-lite/dist/lib/statuses` in OneDrive workspace |
| DOD-24 | Browser end-to-end seeded exploration | NOT_STARTED | Browser test tooling not inspected |
| DOD-25 | Repeatable demo recording flow | NOT_STARTED | — |
| DOD-26 | Setup, architecture, API, voice, audio and demo docs | IN_PROGRESS | Initial docs planned in this slice |
| DOD-27 | Energy and telemetry share engine | IN_PROGRESS | Shared `/api/analysis` handler; integration check pending |
| DOD-28 | Blinded sound-value evaluation exists without efficacy claims | NOT_STARTED | Product evaluation design pending |
