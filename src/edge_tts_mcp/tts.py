"""TTS engine wrapper for edge-tts."""

from dataclasses import dataclass
from pathlib import Path

import edge_tts

from .config import get_settings


@dataclass
class VoiceInfo:
    """Voice information."""

    short_name: str
    gender: str
    locale: str


class TTSEngine:
    """Text-to-speech engine using edge-tts."""

    def __init__(
        self,
        voice: str | None = None,
        rate: str | None = None,
        volume: str | None = None,
        pitch: str | None = None,
    ) -> None:
        settings = get_settings()
        self.voice = voice or settings.voice
        self.rate = rate or settings.rate
        self.volume = volume or settings.volume
        self.pitch = pitch or settings.pitch

    async def generate(self, text: str, output_path: Path) -> None:
        """Generate audio file from text."""
        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice,
            rate=self.rate,
            volume=self.volume,
            pitch=self.pitch,
        )
        await communicate.save(str(output_path))


async def list_voices(language: str | None = None) -> list[VoiceInfo]:
    """List available voices."""
    voices = await edge_tts.list_voices()
    result = []
    for v in voices:
        if language and not v["Locale"].lower().startswith(language.lower()):
            continue
        result.append(VoiceInfo(
            short_name=v["ShortName"],
            gender=v["Gender"],
            locale=v["Locale"],
        ))
    return result
