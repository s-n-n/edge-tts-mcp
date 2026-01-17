# Edge TTS MCP - Документация реализации

## Обзор проекта

**Название:** edge-tts-mcp
**Версия:** 0.1.0
**Назначение:** Кроссплатформенный MCP сервер для Text-to-Speech с использованием Microsoft Edge TTS
**Платформы:** Windows, macOS, Linux
**Статус:** Готов к публикации

## Архитектура

```
edge-tts-mcp/
├── src/edge_tts_mcp/
│   ├── __init__.py      # Экспорт версии (7 строк)
│   ├── __main__.py      # Entry point (6 строк)
│   ├── server.py        # MCP сервер FastMCP (99 строк)
│   ├── tts.py           # TTSEngine обёртка (60 строк)
│   ├── audio.py         # Кроссплатформенные плееры (200 строк)
│   └── config.py        # Pydantic Settings (103 строк)
├── pyproject.toml       # Метаданные и зависимости
├── README.md            # Документация для GitHub
├── INSTALL.md           # Инструкции установки
├── LICENSE              # MIT лицензия
└── .gitignore
```

**Всего:** 475 строк Python кода

## Ключевые компоненты

### server.py - MCP сервер
3 инструмента:
- `speak(text, voice?, rate?, volume?, pitch?)` - озвучить текст
- `list_available_voices(language?)` - список голосов
- `get_config()` - текущие настройки

### audio.py - Аудио плееры
Кроссплатформенные плееры с автоопределением:

| Класс | Платформа | Описание |
|-------|-----------|----------|
| WindowsPlayer | Windows | PowerShell MediaPlayer (встроен) |
| AfplayPlayer | macOS | afplay (встроен) |
| FFPlayPlayer | Все | ffplay из FFmpeg |
| MPVPlayer | Все | mpv плеер |
| PaPlayPlayer | Linux | PulseAudio |

Приоритет автовыбора:
- Windows: windows → ffplay → mpv
- macOS: afplay → ffplay → mpv
- Linux: ffplay → mpv → paplay

### tts.py - TTS движок
- `TTSEngine` - генерация аудио через edge-tts
- `list_voices()` - получение списка голосов

### config.py - Конфигурация
Pydantic Settings с валидацией:
- `voice` = "ru-RU-DmitryNeural"
- `rate` = "+20%"
- `volume` = "+0%"
- `pitch` = "+0Hz"
- `player` = "auto"

## Зависимости

```toml
dependencies = [
    "mcp>=1.0.0",        # MCP протокол
    "edge-tts>=6.1.0",   # Microsoft Edge TTS
    "pydantic-settings>=2.0.0",  # Конфигурация
]
```

## История разработки

### Этап 1: Исследование
- Попытки с VoiceMode MCP - слишком сложно
- Попытки с Kokoro TTS - нет русского языка
- Решение: свой минимальный MCP

### Этап 2: Первая версия (WSL)
- Создан проект с FastMCP
- Проблема: рипы/щелчки при воспроизведении через ffplay в WSL
- Диагностика: проблема в PulseAudio WSL, не в файле
- Решение: WindowsPlayer через PowerShell

### Этап 3: Кроссплатформенность
- Убран WSL - теперь работает на чистом Windows
- Добавлен AfplayPlayer для macOS
- Автоопределение платформы
- Динамические пути (без хардкода)

### Этап 4: Оптимизация
- Удалён лишний код
- Минимизация до 475 строк
- Очистка зависимостей

## Конфигурация для Claude Code

### Windows
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "C:\\Users\\USER\\edge-tts-mcp\\venv\\Scripts\\python.exe",
      "args": ["-m", "edge_tts_mcp"]
    }
  }
}
```

### macOS / Linux
```json
{
  "mcpServers": {
    "edge-tts": {
      "command": "/home/user/edge-tts-mcp/venv/bin/python",
      "args": ["-m", "edge_tts_mcp"]
    }
  }
}
```

## Тестирование

Протестировано:
- ✅ Windows 10/11 (Python 3.13)
- ✅ Русские голоса (Дмитрий, Светлана)
- ✅ Английские термины в русском тексте
- ✅ Разные скорости (+10%, +20%, +25%)
- ✅ Фоновое воспроизведение без GUI

## Публикация

### Перед публикацией на GitHub:
1. Заменить `YOUR_USERNAME` в README.md и pyproject.toml
2. Указать email в pyproject.toml
3. Создать репозиторий на GitHub
4. `git init && git add . && git commit -m "Initial commit"`
5. `git remote add origin ...`
6. `git push -u origin main`

### Структура репозитория:
```
edge-tts-mcp/
├── src/
├── tests/
├── pyproject.toml
├── README.md
├── INSTALL.md
├── LICENSE
└── .gitignore
```

---
*Последнее обновление: Январь 2026*
*Версия: 0.1.0 - кроссплатформенная*
