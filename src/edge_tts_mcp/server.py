"""MCP server for Edge TTS."""

import tempfile
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .audio import play_audio, get_available_players
from .config import get_settings
from .tts import TTSEngine, list_voices

mcp = FastMCP("edge-tts")


@mcp.tool()
async def speak(
    text: str,
    voice: str | None = None,
    rate: str | None = None,
    volume: str | None = None,
    pitch: str | None = None,
) -> str:
    """
    Speak text aloud using Microsoft Edge TTS.

    Args:
        text: Text to speak
        voice: Voice name (e.g., en-US-AriaNeural, uk-UA-OstapNeural)
        rate: Speech rate (-50% to +100%, e.g., +20%)
        volume: Volume (-50% to +100%, e.g., +10%)
        pitch: Pitch (-50Hz to +50Hz, e.g., +5Hz)

    Returns:
        Confirmation message
    """
    engine = TTSEngine(voice=voice, rate=rate, volume=volume, pitch=pitch)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        temp_path = Path(f.name)

    try:
        await engine.generate(text, temp_path)
        await play_audio(temp_path)
        preview = text[:80] + "..." if len(text) > 80 else text
        return f"Spoken: {preview}"
    finally:
        temp_path.unlink(missing_ok=True)


@mcp.tool()
async def list_available_voices(language: str = "") -> str:
    """
    List available TTS voices.

    Args:
        language: Filter by language code (e.g., en, ru, de). Empty for all.

    Returns:
        List of voices with their details
    """
    lang = language if language else None
    voices = await list_voices(lang)

    if not voices:
        return f"No voices found for language: {language}"

    lines = []
    for v in voices[:20]:  # Limit output
        lines.append(f"{v.short_name} ({v.gender}, {v.locale})")

    result = "\n".join(lines)
    if len(voices) > 20:
        result += f"\n... and {len(voices) - 20} more"

    return result


@mcp.tool()
async def get_config() -> str:
    """
    Get current TTS configuration.

    Returns:
        Current settings
    """
    s = get_settings()
    players = get_available_players()

    return f"""Voice: {s.voice}
Rate: {s.rate}
Volume: {s.volume}
Pitch: {s.pitch}
Player: {s.player}
Available players: {', '.join(players) or 'none'}"""


def run() -> None:
    """Run the MCP server."""
    mcp.run()
