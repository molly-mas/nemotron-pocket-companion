from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    llama_server_url: str = "http://127.0.0.1:8080/v1/chat/completions"
    model_name: str = "NVIDIA-Nemotron-3-Nano-4B-GGUF"
    request_timeout_seconds: float = 8.0
    max_tokens: int = 96
    temperature: float = 0.2
    display_backend: str = "console"
    led_backend: str = "console"
    haptics_backend: str = "console"


def load_config(path: Path) -> Config:
    if not path.exists():
        return Config()
    with path.open(encoding="utf-8") as handle:
        values = json.load(handle)
    allowed = Config.__dataclass_fields__.keys()
    return Config(**{key: value for key, value in values.items() if key in allowed})
