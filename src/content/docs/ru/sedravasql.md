---
title: SedravaSQL
description: Экспериментальная открытая СУБД на Rust и SQLite в экосистеме Sedrava.
---

**Выпуск A30 (28 ноября 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) и [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. Единый проверенный комплект Linux x86-64 из трёх CLI: [загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [установка](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 прошёл приёмку на VDS; ранее A26 прошёл независимый Forgejo CI. COW B32–B36 остаётся исследованием. Не для production.

[Контракт миграций A24](https://github.com/VasiliiBabkin/sedravasql/blob/integration/a26-platform/docs/NATIVE_MIGRATIONS_A24.ru.md) · [Платформа](/ru/platform/)

**SedravaSQL** — отдельный публичный [проект с лицензией Apache-2.0](https://github.com/VasiliiBabkin/sedravasql) в экосистеме Sedrava. Он посвящён памяти **Дмитрия Грабыльникова**.

Две экспериментальные реализации: управляемый key/value API поверх SQLite и независимый NativeLog с ограниченным SQL B28 (main). Страничный B+Tree B25 — отдельный прототип, ещё не backend SQL. Не замена PostgreSQL и не сетевой SQL-сервер.

## Что уже работает

| Возможность | Проверенный объём |
| --- | --- |
| Rust + SQLite | Режим WAL, synchronous=FULL, ограниченные записи ключ/значение |
| Изменение записей | Предпросмотр, CAS по ревизии, PUT/GET/LIST/DELETE |
| Атомарность | Изменение данных, аудит и квитанция фиксируются одной транзакцией |
| Повтор запросов | Ключи идемпотентности и сохранённый ответ приложения |
| Резервные копии | SQLite Backup API, проверка схемы и целостности |
| Ограничения файлов | Приватное создание нового файла в Unix, отказ от symlink/hardlink |
| Связь с Sedrava | SQL API A21, роли и ограниченные последовательные транзакции |

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

## Историческая контрольная точка B31 (24–25 ноября 2026)

**Выпуски на момент контрольной точки B31:** [Sedrava 0.12.0-alpha.2](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2), [SedravaSQL 0.1.0-alpha.1](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.1), Linux x86-64 GNU. Rust — единственная развиваемая реализация Sedrava. Ни один выпуск не объявлен стабильным.

| Контур | Проверенная основа | Состояние |
|---|---|---|
| Sedrava main | [896685c](https://github.com/VasiliiBabkin/sedrava/commit/896685ce31f915d1ab69223f98451c2504792cf7) | 83 Rust-теста, 63 HTTP-запроса A17–A21 |
| SedravaSQL main | [363ccbc](https://github.com/VasiliiBabkin/sedravasql/commit/363ccbc9542ed8e3ecf41e3619f78823ffeb97d4) | NativeLog SQL B28, 67 тестов, Clippy PASS |
| Хранилище research | [a98e709](https://github.com/VasiliiBabkin/sedravasql/commit/a98e709cc591057298818d0972c12cf020054295) | B31, 81 тест, Clippy PASS; не подключено к SQL |

### Что изменилось после выпуска

- B26: повторное использование проверенной схемы при чтении; категория 1,68×, агрегация 1,85× по медианам отдельного опыта.
- B27: прямое декодирование JSON; кеш строк отклонён. Выборка без индекса 2,53×, агрегация 2,04× в серии испытаний.
- B28: диапазонный поиск в BTreeMap журнала; на 2048 ключах выборка 1/8/32 строк — 138,4×/89,7×/37,8× против принудительного полного сканирования (эквивалентный запрос с дополнительным условием). Дисковый B25 не принят как SQL backend.
- B29: отдельный бинарный COW B+Tree, 4 КиБ страницы, прямые адреса, кеш до 64 узлов, атомарные пакеты до 16 операций.
- B30: независимая уплотнённая копия, ревизии и tombstones сохранены. Испытано 20 480 ключей; финальная фаза 50,79 → 10,94 МБ.
- B31: UTF-8 значения до 64 КиБ (inline до 256 байт), проверяемые overflow-цепочки; 960 ключей, 16,08 МБ полезных данных, уплотнение 24,76 → 18,87 МБ. Лимит полезных данных compact_copy 32 МиБ проверен с превышением на один байт.

Эти измерения сделаны на общем VDS, относятся к отдельным нагрузкам и не доказывают универсального ускорения или превосходства над SQLite. Тесты аварийного завершения процесса не подтверждают устойчивость к физическому отключению питания. Публичные архивы не содержат последующих изменений B26–B31; номера этапов не являются версиями выпуска.

### Продолжение исследования

Эти планы B32–B36 исследованы отдельно. COW не принят как основной SQL backend. Следующий шаг хранения — отдельная квалификация дискового интерфейса; релиз A30 сохраняет NativeLog. Не использовать ценные данные.

**Отчёты и исходные измерения:** [B26](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B26_PERFORMANCE.ru.md) · [B27](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B27_PERFORMANCE.ru.md) · [B28](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B28_ORDERED_RANGE.ru.md) · [B28-A](https://github.com/VasiliiBabkin/sedravasql/blob/research/b28-tree-sql/docs/NATIVE_SQL_B28_TREE_EXPERIMENT.ru.md) · [B29](https://github.com/VasiliiBabkin/sedravasql/blob/research/b29-cow-tree/docs/NATIVE_COW_B29.ru.md) · [B30](https://github.com/VasiliiBabkin/sedravasql/blob/research/b30-compact/docs/NATIVE_COW_B30.ru.md) · [B31](https://github.com/VasiliiBabkin/sedravasql/blob/research/b31-overflow/docs/NATIVE_COW_B31.ru.md).
