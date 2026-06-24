# si_archive — API поиска по архиву LibGen

## Аппаратура
Raspberry Pi 4 (arm64), Raspberry Pi OS (Debian 13)

## Данные
- **Файлы книг**: `/mnt/hdd/libgen/libgen/` — папки с числовыми именами (0, 1000, 2000… 497000), внутри файлы с именами MD5
- **Дампы БД**: `/mnt/hdd/si_archive/database/` — сырые .dat.gz из aa_derived_mirror_metadata
- **Торрент-копия**: `/mnt/hdd/libgen/libgen/aa_derived_mirror_metadata_20260208/` — полный торрент (резерв)

## База данных
MariaDB 11.8.6, доступ через `sudo mariadb`.

Таблица `libgenrs_updated` (4.5M записей non‑fiction):
- Индексы: PRIMARY(ID), UNIQUE(MD5), FULLTEXT(Title, Author)
- Поля: MD5, Title, Author, Publisher, Year, Pages, Language, Extension, Filesize, Visible, Coverurl, ID, и др.

## Проект
```
/mnt/hdd/si_archive/
├── .env                 # BASE_MOUNT, DB_* конфиг
├── .gitignore
├── requirements.txt
├── database/            # сырые дампы (gitignored)
│   └── libgen/          # libgenrs_updated
├── app/
│   ├── main.py          # FastAPI(), роутеры, startup/shutdown
│   ├── config.py        # чтение .env
│   ├── db.py            # пул aiomysql
│   ├── routers/
│   │   ├── api.py       # /api/search, /api/file/{md5}
│   │   └── web.py       # / — веб-интерфейс
│   └── templates/
│       └── index.html   # HTML с поиском и пагинацией
└── venv/
```

## API
- `GET /api/search?q=...&limit=20&offset=0` — FULLTEXT-поиск по Title/Author
- `GET /api/file/{md5}` — отдача файла (media type по Extension)
- `GET /` — веб-интерфейс

Поиск: `WHERE MATCH(Title, Author) AGAINST ('+слово*' IN BOOLEAN MODE)`.
Файл: `{BOOKS_DIR}/{floor((ID-1)/1000)*1000}/{md5}`.

## Сборка / разработка
- Python + FastAPI + aiomysql + python-dotenv
- Запуск: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- systemd: `si-archive-api.service` (active, enabled)

## Правила кода
- Без вложенных if-ов, ранний выход из функций/циклов
- Ответы на русском
