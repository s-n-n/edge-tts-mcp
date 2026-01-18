# mcp-edge-tts - Give Claude a Voice!

[![PyPI](https://img.shields.io/pypi/v/mcp-edge-tts)](https://pypi.org/project/mcp-edge-tts/)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macos%20%7C%20linux-lightgrey)](#)

Minimal cross-platform MCP server for text-to-speech using Microsoft Edge TTS.

**Let Claude speak!** Works with Claude Code and Claude Desktop.

Слава Україні!

## Features

- 🎙️ 300+ voices in 50+ languages
- 🖥️ Cross-platform: Windows, macOS, Linux
- 🔑 Zero API keys required
- ⚙️ Customizable: speed, volume, pitch
- 🤖 Works with Claude Code and Claude Desktop

## Installation

### Via pip (recommended)

```bash
pip install mcp-edge-tts
```

### From source

#### Windows

```cmd
git clone https://github.com/s-n-n/edge-tts-mcp.git
cd edge-tts-mcp
python -m venv venv
venv\Scripts\activate
pip install -e .
```

#### macOS / Linux

```bash
git clone https://github.com/s-n-n/edge-tts-mcp.git
cd edge-tts-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

## Setup

Add to your MCP configuration:

### If installed via pip

```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "python",
      "args": ["-m", "mcp_edge_tts"]
    }
  }
}
```

### If installed from source

#### Claude Code (`.mcp.json`)

**Windows:**
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "C:\\path\\to\\edge-tts-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "mcp_edge_tts"]
    }
  }
}
```

**macOS / Linux:**
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "/path/to/edge-tts-mcp/venv/bin/python",
      "args": ["-m", "mcp_edge_tts"]
    }
  }
}
```

## Usage

### speak
Speak text aloud.

```
speak("Hello, world!")
speak("Привіт!", voice="uk-UA-PolinaNeural")
speak("Fast!", rate="+50%")
```

**Parameters:**
| Parameter | Description | Example |
|-----------|-------------|---------|
| `text` | Text to speak | `"Hello"` |
| `voice` | Voice name | `"en-US-AriaNeural"` |
| `rate` | Speed (-50% to +100%) | `"+20%"` |
| `volume` | Volume (-50% to +100%) | `"+10%"` |
| `pitch` | Pitch (-50Hz to +50Hz) | `"+5Hz"` |

### list_available_voices
List voices, optionally filtered by language.

```
list_available_voices()
list_available_voices("uk")
```

### get_config
Show current settings and available audio players.

## Configuration

Set defaults via environment variables or `.env` file:

```bash
EDGE_TTS_VOICE=uk-UA-OstapNeural
EDGE_TTS_RATE=+0%
EDGE_TTS_VOLUME=+0%
EDGE_TTS_PITCH=+0Hz
EDGE_TTS_PLAYER=auto
```

## Audio Players

Auto-detected by platform:

| Platform | Default Player | Alternatives |
|----------|---------------|--------------|
| Windows | PowerShell MediaPlayer (built-in) | ffplay, mpv |
| macOS | afplay (built-in) | ffplay, mpv |
| Linux | ffplay | mpv, paplay |

## Popular Voices

| Language | Voice | Gender |
|----------|-------|--------|
| Ukrainian | uk-UA-OstapNeural | Male |
| Ukrainian | uk-UA-PolinaNeural | Female |
| English (US) | en-US-AriaNeural | Female |
| English (US) | en-US-GuyNeural | Male |
| German | de-DE-ConradNeural | Male |
| French | fr-FR-DeniseNeural | Female |
| Spanish | es-ES-AlvaroNeural | Male |
| Chinese | zh-CN-XiaoxiaoNeural | Female |

Run `list_available_voices()` for full list.

## Requirements

- Python 3.10+
- No additional software on Windows/macOS (uses built-in players)
- Linux: `ffmpeg` or `mpv` recommended

## License

MIT

---

Made with ❤️ in Ukraine
