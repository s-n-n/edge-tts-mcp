"""Cross-platform audio playback backends."""

import asyncio
import shutil
import sys
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal

from .config import get_settings

PlayerType = Literal["auto", "ffplay", "mpv", "paplay", "afplay", "windows"]

PLATFORM = sys.platform  # 'win32', 'darwin', 'linux'


class AudioPlayer(ABC):
    """Abstract base class for audio players."""

    name: str

    @classmethod
    @abstractmethod
    def is_available(cls) -> bool:
        """Check if this player is available on the system."""
        ...

    @abstractmethod
    async def play(self, audio_path: Path) -> None:
        """Play audio file."""
        ...


class FFPlayPlayer(AudioPlayer):
    """FFplay audio player (from FFmpeg). Works on all platforms."""

    name = "ffplay"

    @classmethod
    def is_available(cls) -> bool:
        return shutil.which("ffplay") is not None

    async def play(self, audio_path: Path) -> None:
        process = await asyncio.create_subprocess_exec(
            "ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet",
            str(audio_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()


class MPVPlayer(AudioPlayer):
    """MPV audio player. Works on all platforms."""

    name = "mpv"

    @classmethod
    def is_available(cls) -> bool:
        return shutil.which("mpv") is not None

    async def play(self, audio_path: Path) -> None:
        process = await asyncio.create_subprocess_exec(
            "mpv", "--no-video", "--really-quiet", str(audio_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()


class AfplayPlayer(AudioPlayer):
    """macOS afplay player (built-in)."""

    name = "afplay"

    @classmethod
    def is_available(cls) -> bool:
        return PLATFORM == "darwin" and shutil.which("afplay") is not None

    async def play(self, audio_path: Path) -> None:
        process = await asyncio.create_subprocess_exec(
            "afplay", str(audio_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()


class PaPlayPlayer(AudioPlayer):
    """PulseAudio paplay player (Linux)."""

    name = "paplay"

    @classmethod
    def is_available(cls) -> bool:
        return PLATFORM == "linux" and shutil.which("paplay") is not None

    async def play(self, audio_path: Path) -> None:
        if audio_path.suffix.lower() == ".mp3":
            if not shutil.which("ffmpeg"):
                raise RuntimeError("ffmpeg required for mp3 playback")
            cmd = f'ffmpeg -i "{audio_path}" -f wav - 2>/dev/null | paplay'
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
        else:
            process = await asyncio.create_subprocess_exec(
                "paplay", str(audio_path),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
        await process.wait()


class WindowsPlayer(AudioPlayer):
    """Windows media player via PowerShell (native Windows)."""

    name = "windows"

    @classmethod
    def is_available(cls) -> bool:
        return PLATFORM == "win32"

    async def play(self, audio_path: Path) -> None:
        # Use Windows temp directory
        temp_dir = Path(tempfile.gettempdir())
        temp_audio = temp_dir / f"edge_tts_{audio_path.name}"
        shutil.copy2(audio_path, temp_audio)

        script = f'''Add-Type -AssemblyName PresentationCore
$p = New-Object System.Windows.Media.MediaPlayer
$p.Open("{temp_audio}")
$p.Play()
Start-Sleep -Milliseconds 500
while ($p.Position -lt $p.NaturalDuration.TimeSpan) {{ Start-Sleep -Milliseconds 100 }}
$p.Close()
Remove-Item "{temp_audio}" -ErrorAction SilentlyContinue
'''
        script_path = temp_dir / "edge_tts_play.ps1"
        script_path.write_text(script)

        process = await asyncio.create_subprocess_exec(
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str(script_path),
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.DEVNULL,
        )
        await process.wait()


# Player registry
PLAYERS: dict[str, type[AudioPlayer]] = {
    "ffplay": FFPlayPlayer,
    "mpv": MPVPlayer,
    "afplay": AfplayPlayer,
    "paplay": PaPlayPlayer,
    "windows": WindowsPlayer,
}

# Platform-specific player priority
PLAYER_PRIORITY = {
    "win32": ["windows", "ffplay", "mpv"],
    "darwin": ["afplay", "ffplay", "mpv"],
    "linux": ["ffplay", "mpv", "paplay"],
}


def get_available_players() -> list[str]:
    """Get list of available audio players."""
    return [name for name, cls in PLAYERS.items() if cls.is_available()]


def get_player(player_type: PlayerType | None = None) -> AudioPlayer:
    """Get audio player instance."""
    if player_type is None:
        player_type = get_settings().player

    if player_type != "auto":
        if player_type not in PLAYERS:
            raise ValueError(f"Unknown player: {player_type}")
        player_cls = PLAYERS[player_type]
        if not player_cls.is_available():
            raise RuntimeError(f"Player not available: {player_type}")
        return player_cls()

    # Auto-select based on platform
    priority = PLAYER_PRIORITY.get(PLATFORM, ["ffplay", "mpv"])
    for name in priority:
        if PLAYERS[name].is_available():
            return PLAYERS[name]()

    raise RuntimeError("No audio player available")


async def play_audio(audio_path: Path, player_type: PlayerType | None = None) -> None:
    """Play audio file."""
    await get_player(player_type).play(audio_path)
