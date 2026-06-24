# libgen — non‑fiction metadata

**Источник:** Anna's Archive `aa_derived_mirror_metadata_20260208`
**Дата дампа:** февраль 2026
**Записей:** 4 530 301
**Таблица:** `libgenrs_updated`

## Импорт

```sql
CREATE DATABASE IF NOT EXISTS libgen CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci;

zcat schema.sql.gz | sudo mariadb libgen

sudo mariadb --local-infile=1 libgen -e "
LOAD DATA INFILE 'data.dat.gz'
INTO TABLE libgenrs_updated
CHARACTER SET utf8mb3
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' ESCAPED BY '\\\\'
LINES STARTING BY '' TERMINATED BY '\n'
IGNORE 1 LINES;
"
```

## Индексы

- `PRIMARY` — ID
- `UNIQUE` — MD5
- `FULLTEXT` — Title, Author

## Формат файла

- `.dat.gz` — CSV, поля разделены `,`, значения в `"`, экранирование `\`
- `.sql.gz` — обёртка для `LOAD DATA LOCAL INFILE`
- `-schema.sql.gz` — `CREATE TABLE`
