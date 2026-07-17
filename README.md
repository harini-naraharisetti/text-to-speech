# Text to Speech

Natural neural voices in 40+ languages, streamed straight to an audio element. Free, no key.

**5 of 10** — part of a GenAI project series. FastAPI backend, vanilla JS frontend.

## What it demonstrates

- Async audio synthesis and streaming binary responses from FastAPI
- Voice, rate, and pitch control (SSML-style prosody)
- Serving generated media without writing to disk

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
# add your key to .env  (skip if this project needs no key)
uvicorn main:app --reload
```

Open http://127.0.0.1:8000

## Keys

**None.** `edge-tts` uses Microsoft Edge's public read-aloud voices and needs no account or key.

It does need an internet connection — the synthesis happens on Microsoft's side.

## Stack

FastAPI · edge-tts

## How it works

`edge-tts` streams MP3 chunks over a websocket. `main.py` collects them into an in-memory buffer and returns it as `audio/mpeg`, so nothing touches the filesystem. `/api/voices` lists every available voice so the dropdown is populated from the real catalogue rather than hardcoded.

---
MIT
