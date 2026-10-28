# Decisions

- **Initial slice is an in-memory API.** Keeping seeded datasets inspectable and the first end-to-end slice small makes analytics behavior easy to verify. SQLite persistence is still required and is a follow-up milestone.
- **Use custom Web Audio tones.** Numeric value maps linearly to oscillator pitch; event-focused mode uses a triangle timbre while trend uses sine. No speech or external audio assets are represented as data sonification.
- **Synthetic seeds are explicit.** Household and API series are generated deterministically and labeled synthetic in the API/UI.
- **Voice is disabled until integrated.** No browser speech synthesis or fixture is represented as Gnani. Live STT/TTS requires a server-side provider adapter and credentials.
- **Energy seed stores interval kWh.** The labeled ₹8/kWh demo tariff is configurable in the analysis API, and cost multiplies interval quantities directly; raw kW is not treated as energy.
- **Comparison aligns equal offsets in two adjacent equal-length windows.** It reports per-offset differences and a mean difference in the metric's unit; it does not imply causation.
- **Local intent is constrained deterministic routing.** A bounded phrase-to-tool layer provides inspectable analysis while the live speech path awaits verified provider adapters; the UI labels its local nature.
