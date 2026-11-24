---
title: SedravaSQL
description: Экспериментальная открытая СУБД на Rust и SQLite в экосистеме Sedrava.
---

**SedravaSQL** — отдельный публичный [проект с лицензией Apache-2.0](https://github.com/VasiliiBabkin/sedravasql) в экосистеме Sedrava. Он посвящён памяти **Дмитрия Грабыльникова**.

Две экспериментальные реализации: управляемый key/value API поверх SQLite и независимый NativeLog с ограниченным SQL B23. Страничный B+Tree B25 — отдельный прототип, ещё не backend SQL. Не замена PostgreSQL и не сетевой SQL-сервер.

## Что уже работает

| Возможность | Проверенный объём |
| --- | --- |
| Rust + SQLite | Режим WAL, synchronous=FULL, ограниченные записи ключ/значение |
| Изменение записей | Предпросмотр, CAS по ревизии, PUT/GET/LIST/DELETE |
| Атомарность | Изменение данных, аудит и квитанция фиксируются одной транзакцией |
| Повтор запросов | Ключи идемпотентности и сохранённый ответ приложения |
| Резервные копии | SQLite Backup API, проверка схемы и целостности |
| Ограничения файлов | Приватное создание нового файла в Unix, отказ от symlink/hardlink |
| Связь с Sedrava | Экспериментальные серверы A5/A6; в A6 — оператор чтения db_get |

Это реализованные механизмы, **не доказательство абсолютной сохранности данных**, защиты от злоумышленника с тем же системным пользователем или сертификат безопасности.

## Попробовать локально

При наличии Rust и Cargo:

~~~sh
git clone https://github.com/VasiliiBabkin/sedravasql.git
cd sedravasql
cargo build --locked
cargo test --locked --all-targets
python3 scripts/verify_local.py
~~~

Пример с тестовой базой. Используйте отдельный приватный каталог и не подставляйте путь к важным данным:

~~~sh
mkdir -m 700 -p /tmp/sedravasql-example
DB=/tmp/sedravasql-example/data.sqlite
BIN=./target/debug/sedravasql
"$BIN" init "$DB"
"$BIN" put "$DB" example welcome "Привет от SedravaSQL" --expect 0 --request-key example-request-0001
"$BIN" get "$DB" example welcome
"$BIN" verify "$DB"
"$BIN" backup "$DB" /tmp/sedravasql-example/backup.sqlite
~~~

## Независимый SQL

NativeLog: типизированные таблицы, SELECT/INSERT/UPDATE/DELETE, JOIN, агрегаты, GROUP BY/HAVING, DISTINCT, вторичные индексы, внешние ключи и ограниченные последовательные транзакции. B24/B25: отдельные изменяемые страницы, redo WAL, кеш, разделение узлов B+Tree. SQL пока работает на журнале; слияние узлов и интеграция остаются задачами.

[Официальный сайт и загрузки](https://sql.virtreal.ru/) · [SQL B23](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B23.ru.md) · [B25](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_TREE_B25.ru.md) · [Измерения](/ru/benchmarks/). Не используйте ценные данные.
