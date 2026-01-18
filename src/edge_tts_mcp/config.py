"""Configuration management using pydantic-settings."""

from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="EDGE_TTS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Voice settings
    voice: str = Field(
        default="uk-UA-PolinaNeural",
        description="Default TTS voice",
    )
    rate: str = Field(
        default="+20%",
        description="Speech rate (-50% to +100%)",
    )
    volume: str = Field(
        default="+0%",
        description="Volume (-50% to +100%)",
    )
    pitch: str = Field(
        default="+0Hz",
        description="Pitch (-50Hz to +50Hz)",
    )

    # Audio player
    player: Literal["auto", "ffplay", "mpv", "paplay", "afplay", "windows"] = Field(
        default="auto",
        description="Audio player backend",
    )

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = Field(
        default="INFO",
        description="Logging level",
    )

    @field_validator("rate")
    @classmethod
    def validate_rate(cls, v: str) -> str:
        """Validate rate format."""
        if not v.endswith("%"):
            raise ValueError("Rate must end with % (e.g., +10%, -20%)")
        try:
            val = int(v[:-1].replace("+", ""))
            if not -50 <= val <= 100:
                raise ValueError("Rate must be between -50% and +100%")
        except ValueError as e:
            if "Rate must" in str(e):
                raise
            raise ValueError("Invalid rate format. Use +10% or -20%") from e
        return v

    @field_validator("volume")
    @classmethod
    def validate_volume(cls, v: str) -> str:
        """Validate volume format."""
        if not v.endswith("%"):
            raise ValueError("Volume must end with % (e.g., +10%, -20%)")
        try:
            val = int(v[:-1].replace("+", ""))
            if not -50 <= val <= 100:
                raise ValueError("Volume must be between -50% and +100%")
        except ValueError as e:
            if "Volume must" in str(e):
                raise
            raise ValueError("Invalid volume format. Use +10% or -20%") from e
        return v

    @field_validator("pitch")
    @classmethod
    def validate_pitch(cls, v: str) -> str:
        """Validate pitch format."""
        if not v.endswith("Hz"):
            raise ValueError("Pitch must end with Hz (e.g., +10Hz, -5Hz)")
        try:
            val = int(v[:-2].replace("+", ""))
            if not -50 <= val <= 50:
                raise ValueError("Pitch must be between -50Hz and +50Hz")
        except ValueError as e:
            if "Pitch must" in str(e):
                raise
            raise ValueError("Invalid pitch format. Use +10Hz or -5Hz") from e
        return v


_settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return _settings
