import re
from io import BytesIO

from gtts import gTTS


def _clean(text: str) -> str:
    # Clean up whitespace for better TTS processing
    return re.sub(r"\s+", " ", text).strip()


def text_to_speech(text: str):
    cleaned = _clean(text)
    tts = gTTS(cleaned)
    bio = BytesIO()
    tts.write_to_fp(bio)
    bio.seek(0)
    return bio.read(), "audio/mp3"
