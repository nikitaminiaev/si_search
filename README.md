# si-archive

Поиск и отдача файлов из архива LibGen (non‑fiction) через веб-интерфейс и REST API.

## Запуск

```bash
cd /mnt/hdd/si_archive
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Через systemd (автозапуск):

```bash
sudo systemctl start si-archive-api.service
```

## API

```
GET /api/search?q={запрос}&limit=20&offset=0
GET /api/file/{md5}
```

## Данные

- Книжные файлы: `/mnt/hdd/libgen/libgen/`
- Дампы БД: `database/libgen/`
- Торрент-копия: `/mnt/hdd/libgen/libgen/aa_derived_mirror_metadata_20260208/`

## Конфигурация

Настройки в `.env` (не в git):

```
BASE_MOUNT=/mnt/hdd
DB_USER=libgen
DB_PASSWORD=libgen
```

## Стек

- Python 3 + FastAPI + aiomysql
- MariaDB 11 + MyISAM + FULLTEXT
- Установка: `pip install -r requirements.txt`
