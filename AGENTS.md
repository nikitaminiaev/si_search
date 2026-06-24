# si_archive — API поиска по архиву LibGen

## Аппаратура
Raspberry Pi 4 (arm64), Raspberry Pi OS (Debian 13)

## Данные
- **Файлы книг**: `/mnt/hdd/libgen/libgen/` — разложены по папкам с числовыми именами (0, 1000, 10000… 99000), внутри файлы с именами MD5
- **SQL дампы БД**: `/mnt/hdd/si_archive/libgen_is_db/` — libgen_2025-06-25.rar и fiction_2025-06-25.rar
  - libgen — основная non-fiction (~6.5M записей)
  - fiction — художественная (~2.5M записей)
  - Источник: https://libgen.la/torrents/libgen_is_db/

## База данных
MariaDB 11.8.6, уже запущена. Доступ через `sudo mariadb`.

Таблицы после импорта:
- `libgen` (в дампе название может отличаться, обычно `libgen` или `updated`)
- Поля: md5, title, author, publisher, year, pages, language, filesize, extension, topic, identifier, coverurl
- `fiction` — аналогично для художественной литературы

## API
FastAPI приложение для поиска. Маршруты:
- `GET /search?q=...` — поиск по названию/автору
- `GET /file/{md5}` — получение файла (опционально)

## Сборка / разработка
- Python + FastAPI + asyncmy/aiomysql для асинхронного доступа к БД
- Запуск: `uvicorn api:app --host 0.0.0.0 --port 8000`

## Правила кода
- Без вложенных if-ов, ранний выход из функций/циклов
- Ответы на русском
