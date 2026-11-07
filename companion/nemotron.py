from __future__ import annotations

import json
import urllib.request

from .config import Config
from .reactions import Reaction, SYSTEM_PROMPT, fallback, parse_reaction


class NemotronClient:
    """Tiny client for llama.cpp's OpenAI-compatible local server API."""

    def __init__(self, config: Config):
        self.config = config

    def choose_reaction(self, event: str) -> Reaction:
        payload = {
            "model": self.config.model_name,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Event label: {event[:80]}\nChoose a reaction."},
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens,
            "stream": False,
        }
        request = urllib.request.Request(
            self.config.llama_server_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.config.request_timeout_seconds) as response:
                result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return parse_reaction(content, event)
        except Exception as exc:
            # Keep device interactions available even if inference is slow/offline.
            print(f"[Nemotron unavailable: {type(exc).__name__}; using local fallback]")
            return fallback(event)
