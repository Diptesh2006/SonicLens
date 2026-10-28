# Gnani Prisma and Timbre setup

The API has server-side adapters for Prisma v3 streaming STT and Timbre REST TTS, following the official [Prisma streaming](https://docs.gnani.ai/api/STT/stt-websocket) and [Timbre inference](https://docs.gnani.ai/api/TTS/tts-inference) contracts. The browser sends microphone PCM only to the local API; Gnani credentials are never sent to the browser.

Configure the API process environment before starting Uvicorn:

```powershell
$env:GNANI_API_KEY = "your Gnani API key"
$env:GNANI_PRISMA_MODEL = "prisma-v3.0"
$env:GNANI_TIMBRE_MODEL = "timbre-v2.5"
$env:GNANI_TIMBRE_VOICE = "Nalini"
uvicorn main:app --reload --port 8000
```

Optional endpoint overrides are `GNANI_PRISMA_URL` (defaults to `wss://api.vachana.ai/stt/v3/stream`) and `GNANI_TIMBRE_URL` (defaults to `https://api.vachana.ai/api/v1/tts/inference`). The UI checks `/api/health` and enables microphone capture only when `GNANI_API_KEY` is present.

Prisma receives 16-bit mono PCM frames paced at the chosen sample rate, with `x-api-key-id`, `x-model`, `lang_code`, `x-sample-rate`, and `x-format` handshake headers. The browser currently captures 16 kHz mono audio for up to 12 seconds. Timbre receives the evidence-grounded deterministic answer and requests mono 48 kHz WAV; the API verifies a RIFF WAV response before returning it for playback.

No live authenticated Prisma or Timbre call has been verified in this environment: no `GNANI_*` variables were configured at implementation time. Automated provider tests mock the external requests and are not live integration evidence. Provider/model availability and account permissions must be confirmed with the supplied credentials.
