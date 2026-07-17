import io, os
import edge_tts
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI(title="Text to Speech")
DEFAULT_VOICE = os.getenv("DEFAULT_VOICE", "en-US-AriaNeural")

_voice_cache = None


@app.get("/api/voices")
async def voices():
    """The real catalogue, so the dropdown never goes stale."""
    global _voice_cache
    if _voice_cache is None:
        raw = await edge_tts.list_voices()
        _voice_cache = sorted(
            (
                {
                    "name": v["ShortName"],
                    "gender": v["Gender"],
                    "locale": v["Locale"],
                }
                for v in raw
            ),
            key=lambda v: v["name"],
        )
    return _voice_cache


class Speech(BaseModel):
    text: str
    voice: str = DEFAULT_VOICE
    rate: int = 0     # percent, -50 to +100
    pitch: int = 0    # Hz, -50 to +50


async def synth(text: str, voice: str, rate: int = 0, pitch: int = 0) -> bytes:
    """Shared by this project and the voice assistant (#07)."""
    comm = edge_tts.Communicate(
        text,
        voice,
        rate=f"{rate:+d}%",
        pitch=f"{pitch:+d}Hz",
    )
    buf = io.BytesIO()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    return buf.getvalue()


@app.post("/api/speak")
async def speak(body: Speech):
    if not body.text.strip():
        raise HTTPException(400, "Enter some text to speak.")
    if len(body.text) > 5000:
        raise HTTPException(400, "Text is over the 5000 character limit.")

    audio = await synth(body.text, body.voice, body.rate, body.pitch)
    return Response(
        content=audio,
        media_type="audio/mpeg",
        headers={"Content-Disposition": 'inline; filename="speech.mp3"'},
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
