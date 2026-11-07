from __future__ import annotations

import json
import re
from dataclasses import dataclass

EMOTIONS = {"proud", "calm", "curious", "supportive", "playful"}
FACES = {"happy", "calm", "curious", "sleepy", "encourage"}
LED_PATTERNS = {"off", "calm", "success", "encourage", "celebrate"}
HAPTIC_PATTERNS = {"off", "soft", "success", "double_tap"}
MAX_MESSAGE_LENGTH = 48


@dataclass(frozen=True)
class Reaction:
    emotion: str
    face: str
    led: str
    haptic: str
    message: str


SYSTEM_PROMPT = """You select a gentle, supportive reaction for a small wellbeing toy.
Return exactly one JSON object with keys emotion, face, led, haptic, message.
Allowed emotion: proud, calm, curious, supportive, playful.
Allowed face: happy, calm, curious, sleepy, encourage.
Allowed led: off, calm, success, encourage, celebrate.
Allowed haptic: off, soft, success, double_tap.
Message: at most 8 words, kind and non-clinical. Infer no diagnosis or mood.
Output JSON only. Never request raw GPIO settings or stronger/longer motor use."""


def fallback(event: str) -> Reaction:
    event = event.strip().lower()
    if event == "task_done":
        return Reaction("proud", "happy", "success", "success", "Nice work!")
    if event == "shake":
        return Reaction("playful", "curious", "celebrate", "double_tap", "Hello there!")
    if event == "idle":
        return Reaction("calm", "calm", "calm", "off", "A little pause is okay.")
    if event == "button":
        return Reaction("curious", "curious", "encourage", "soft", "What shall we try?")
    return Reaction("supportive", "encourage", "encourage", "soft", "One small step is enough.")


def parse_reaction(text: str, event: str) -> Reaction:
    """Extract and strictly validate the model response; fall back on any issue."""
    try:
        match = re.search(r"\{.*?\}", text, flags=re.DOTALL)
        if not match:
            return fallback(event)
        data = json.loads(match.group(0))
        emotion, face = data["emotion"], data["face"]
        led, haptic = data["led"], data["haptic"]
        message = " ".join(str(data.get("message", "" )).split())[:MAX_MESSAGE_LENGTH]
        if emotion not in EMOTIONS or face not in FACES or led not in LED_PATTERNS or haptic not in HAPTIC_PATTERNS:
            return fallback(event)
        return Reaction(emotion, face, led, haptic, message)
    except (ValueError, TypeError, KeyError):
        return fallback(event)
