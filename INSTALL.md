# Установка Edge TTS MCP

Кроссплатформенный MCP сервер для Text-to-Speech.

## Требования

- Python 3.10+
- Claude Code

## Windows

### 1. Установи Python
Скачай с https://python.org и установи (отметь "Add to PATH")

### 2. Клонируй и установи
```cmd
cd %USERPROFILE%
git clone https://github.com/YOUR_USERNAME/edge-tts-mcp.git
cd edge-tts-mcp
python -m venv venv
venv\Scripts\activate
pip install -e .
```

### 3. Настрой Claude Code
В `.mcp.json` проекта:
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "C:\\Users\\YOUR_USER\\edge-tts-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "edge_tts_mcp"]
    }
  }
}
```

## macOS

### 1. Установи Python
```bash
brew install python
```

### 2. Клонируй и установи
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/edge-tts-mcp.git
cd edge-tts-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. Настрой Claude Code
В `.mcp.json` проекта:
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "/Users/YOUR_USER/edge-tts-mcp/venv/bin/python",
      "args": ["-m", "edge_tts_mcp"]
    }
  }
}
```

## Linux

### 1. Установи Python и ffmpeg
```bash
sudo apt install python3 python3-venv ffmpeg
```

### 2. Клонируй и установи
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/edge-tts-mcp.git
cd edge-tts-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. Настрой Claude Code
В `.mcp.json` проекта:
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "/home/YOUR_USER/edge-tts-mcp/venv/bin/python",
      "args": ["-m", "edge_tts_mcp"]
    }
  }
}
```

## Проверка

После перезапуска Claude Code:
```
mcp__edge-tts__speak(text="Привет! Установка прошла успешно.")
```

## Настройка голоса

Через `.env` файл в папке проекта:
```
EDGE_TTS_VOICE=ru-RU-DmitryNeural
EDGE_TTS_RATE=+20%
```

Или при вызове:
```
mcp__edge-tts__speak(text="Текст", voice="ru-RU-SvetlanaNeural", rate="+25%")
```

## Доступные голоса

**Русские:**
- `ru-RU-DmitryNeural` - мужской
- `ru-RU-SvetlanaNeural` - женский

**Английские:**
- `en-US-GuyNeural` - мужской
- `en-US-JennyNeural` - женский

Полный список: `mcp__edge-tts__list_available_voices(language="en")`

## Аудио плееры

Автоматический выбор по платформе:
- **Windows**: PowerShell MediaPlayer (встроен)
- **macOS**: afplay (встроен)
- **Linux**: ffplay (нужен ffmpeg)

## Troubleshooting

### Windows: нет звука
Убедись что PowerShell работает: `powershell -Command "echo test"`

### macOS: нет звука
Проверь afplay: `afplay /System/Library/Sounds/Ping.aiff`

### Linux: нет звука
Установи ffmpeg: `sudo apt install ffmpeg`
