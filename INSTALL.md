# Встановлення Edge TTS MCP

Кросплатформний MCP сервер для Text-to-Speech.

## Вимоги

- Python 3.10+
- Claude Code

## Windows

### 1. Встанови Python
Завантаж з https://python.org та встанови (відміть "Add to PATH")

### 2. Клонуй та встанови
```cmd
cd %USERPROFILE%
git clone https://github.com/s-n-n/edge-tts-mcp.git
cd edge-tts-mcp
python -m venv venv
venv\Scripts\activate
pip install -e .
```

### 3. Налаштуй Claude Code
В `.mcp.json` проєкту:
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

### 1. Встанови Python
```bash
brew install python
```

### 2. Клонуй та встанови
```bash
cd ~
git clone https://github.com/s-n-n/edge-tts-mcp.git
cd edge-tts-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. Налаштуй Claude Code
В `.mcp.json` проєкту:
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

### 1. Встанови Python та ffmpeg
```bash
sudo apt install python3 python3-venv ffmpeg
```

### 2. Клонуй та встанови
```bash
cd ~
git clone https://github.com/s-n-n/edge-tts-mcp.git
cd edge-tts-mcp
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 3. Налаштуй Claude Code
В `.mcp.json` проєкту:
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

## Перевірка

Після перезапуску Claude Code:
```
speak("Привіт! Встановлення пройшло успішно.")
```

## Налаштування голосу

Через `.env` файл в папці проєкту:
```
EDGE_TTS_VOICE=uk-UA-OstapNeural
EDGE_TTS_RATE=+20%
```

Або при виклику:
```
speak("Текст", voice="uk-UA-OstapNeural", rate="+25%")
```

## Доступні голоси

**Українські:**
- `uk-UA-OstapNeural` - чоловічий (за замовчуванням)
- `uk-UA-PolinaNeural` - жіночий

**Англійські:**
- `en-US-AriaNeural` - жіночий
- `en-US-GuyNeural` - чоловічий

Повний список: `list_available_voices("uk")`

## Аудіо плеєри

Автоматичний вибір за платформою:
- **Windows**: PowerShell MediaPlayer (вбудований)
- **macOS**: afplay (вбудований)
- **Linux**: ffplay (потрібен ffmpeg)

## Вирішення проблем

### Windows: немає звуку
Переконайся що PowerShell працює: `powershell -Command "echo test"`

### macOS: немає звуку
Перевір afplay: `afplay /System/Library/Sounds/Ping.aiff`

### Linux: немає звуку
Встанови ffmpeg: `sudo apt install ffmpeg`

---

Слава Україні!
