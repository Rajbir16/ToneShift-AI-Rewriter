import os
import time
from dataclasses import dataclass

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


@dataclass
class GroqStatus:
    ok: bool
    error: str = None
    model: str = None



class GroqClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self._api_key_missing = not api_key
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self._client = None
        if api_key:
            self._client = Groq(api_key=api_key)

    @property
    def connected(self) -> bool:
        return self._client is not None and not self._api_key_missing

    def test_connection(self) -> GroqStatus:
        if self._api_key_missing:
            return GroqStatus(ok=False, error="Missing GROQ_API_KEY")

        try:
            # lightweight call
            self._client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Say OK"}],
                temperature=0.0,
                max_tokens=5,
            )
            return GroqStatus(ok=True, model=self.model)
        except Exception as e:
            msg = str(e)
            # heuristic mapping
            if "401" in msg or "authentication" in msg.lower():
                return GroqStatus(ok=False, error="Invalid API key")
            if "rate limit" in msg.lower():
                return GroqStatus(ok=False, error="Rate limit")
            if "timeout" in msg.lower():
                return GroqStatus(ok=False, error="Timeout")
            return GroqStatus(ok=False, error="Network failure")

    def rewrite(self, prompt: str) -> str:
        if self._api_key_missing:
            raise RuntimeError("Missing GROQ_API_KEY")

        # retry with backoff
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                resp = self._client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.4,
                )
                return resp.choices[0].message.content.strip()
            except Exception as e:
                last_err = e
                time.sleep(1.2 * (attempt + 1))

        raise RuntimeError(f"Groq request failed: {last_err}")
