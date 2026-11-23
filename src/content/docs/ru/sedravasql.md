---
title: SedravaSQL
description: Экспериментальная открытая СУБД на Rust и SQLite в экосистеме Sedrava.
---

**SedravaSQL** — отдельный публичный [проект с лицензией Apache-2.0](https://github.com/VasiliiBabkin/sedravasql) в экосистеме Sedrava. Он посвящён памяти **Дмитрия Грабыльникова**.

Сейчас реализованы **экспериментальная Rust-библиотека и CLI на базе SQLite**, а не замена PostgreSQL, сетевой SQL-сервер или промышленная универсальная СУБД. Интерфейс пока ограничен типизированными ключами и значениями, версионированной схемой и проверяемыми операциями изменения.

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

## Архитектура и развитие

В Rust API также появилось атомарное сохранение ограниченного JSON-ответа приложения вместе с квитанцией изменения. Такие квитанции **не удаляются автоматически**. Нативный [сервер Sedrava A6](/ru/rust-native/) применяет этот механизм для безопасного повтора HTTP-запросов после перезапуска. Оператора записи в базу из самого языка Sedrava пока нет.

**Остаются задачи:** типизированные многоключевые транзакции, миграции, квоты, архивирование квитанций, проверки на разных ОС, реальные тесты отключения питания, аутентификация и безопасная публикация серверов. Для важных производственных данных текущая версия не предназначена.

[Исходники и запуск](https://github.com/VasiliiBabkin/sedravasql) · [Реализованные возможности](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/IMPLEMENTED_V0_1.ru.md) · [Протокол проверки](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/VERIFICATION.md) · [План разработки](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/ROADMAP.md)
