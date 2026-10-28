# Gnani Prisma and Timbre setup

## Add your key

Open the repository-root `.env` file and set:

```dotenv
GNANI_API_KEY=paste-your-key-here
```

The API loads this file on startup. `.env` is ignored by Git; keep the key there or in the API process environment. Never put the key in frontend code, a checked-in file, screenshots, or chat. Restart Uvicorn after changing it. The safe template is `.env.example`.

Optional model and endpoint settings:

```dotenv
GNANI_PRISMA_URL=
GNANI_TIMBRE_URL=
GNANI_PRISMA_MODEL=prisma-v3.0
GNANI_TIMBRE_MODEL=timbre-v2.5
GNANI_TIMBRE_VOICE=Nalini
```

Empty endpoint values use the defaults: `wss://api.vachana.ai/stt/v3/stream` for Prisma and `https://api.vachana.ai/api/v1/tts/inference` for Timbre. Use model/voice identifiers enabled for your account.

The browser sends microphone PCM only to the local API. Credentials stay server-side. The UI checks `/api/health` and enables microphone capture only when the API reports the key configured.

Prisma receives 16-bit mono PCM frames paced at the selected sample rate, using `x-api-key-id`, `x-model`, `lang_code`, `x-sample-rate` and `x-format` handshake headers. Browser capture is 16 kHz mono and limited to 12 seconds. Timbre receives the evidence-grounded answer and requests mono 48 kHz WAV; the API validates a RIFF WAV response before returning it.

To try voice, start Uvicorn after editing `.env`, refresh the app, and check that the voice status says “Gnani ready.” Then record a short English prompt. A successful configuration check does not prove the live provider call; model entitlement, language support, network, and account credits still affect the request.
