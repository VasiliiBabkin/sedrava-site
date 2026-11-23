---
title: Нативная версия на Rust
description: Экспериментальная самостоятельная реализация Sedrava на Rust и локальный сервер A6.
---

В [основном репозитории Sedrava](https://github.com/VasiliiBabkin/sedrava) развивается **самостоятельная нативная реализация на Rust**. Она охватывает проверяемые части ядра языка, Web, Android, Host и серверных возможностей. Это **экспериментальная разработка**, а не новый стабильный релиз и не доказанная полная замена опубликованной Python-версии **0.11.0**.

**Опубликованная версия:** [0.11.0 на GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) и [PyPI](https://pypi.org/project/sedrava/0.11.0/). Исторические [0.10.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) ([PyPI](https://pypi.org/project/sedrava/0.10.0/)) и [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) ([PyPI](https://pypi.org/project/sedrava/0.11.0rc1/)) также доступны. Экспериментальная 0.12.0a1 не является опубликованным стабильным выпуском.

## Сборка экспериментальной версии

Для этого нужны совместимые Rust и Cargo:

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --bin sedrava-native
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
./rust/target/debug/sedrava-native server check examples/native_server/sqlite_a5.sdr
~~~

Бинарник собирается из исходников. **Установка через pip не устанавливает экспериментальный сервер A6 на Rust.** Запущенный нативный бинарник не зависит от Python, хотя отдельные тестовые скрипты используют Python. Проверенный контур A6 — Ubuntu Linux x86_64; совместимость с другими ОС отдельно не подтверждена.

## Этапы серверной реализации

| Режим | Что реализовано | Ограничения |
| --- | --- | --- |
| A1–A2 | Локальный HTTP, типизированное состояние, защищённые снимки | Только localhost |
| A3 | Ключи повторных запросов, ревизии CAS и атомарный снимок | Максимум 32 сохраняемые квитанции |
| A4 | Ограниченный журнал повторного применения записей | Нет checkpoint и доказанной сохранности при сбое питания |
| A5 | Хранилище через SedravaSQL / SQLite, аудит и транзакционные ответы | Прежнее ограничение 32 квитанций |
| **A6** | Отдельные постоянные квитанции SQLite, снят лимит 32; первый оператор чтения БД | Нет автоматической очистки, записи из DSL или авторизации |

A6 — **отдельный режим**, он не конвертирует базы A5 автоматически. Первый прямой оператор обращения к БД доступен только для чтения фиксированного ключа в GET-ответе:

~~~text
server "A6 SQL Read Example"
state enabled: bool = true
route GET "/note":
    respond 200 { note: db_get("public_notes/welcome"), enabled: state.enabled }
~~~

Для запуска потребуется отдельная приватная SQLite-база SedravaSQL и экспериментальный флаг из [документации Server A6](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/RUST_NATIVE_SERVER_A6_SQLITE.ru.md). Это **не публичная интерактивная SQL-песочница**. Оператор не может выполнять произвольные SQL-запросы, менять записи или обращаться к внутренним пространствам имён сервера.

## Проверки и дальнейшие задачи

Зафиксированы **78 Rust-тестов**, реальные HTTP-запросы после превышения порога 32 записей, восстановление ранее сохранённого ответа после перезапуска и четыре *отладочных* принудительных завершения процесса около COMMIT. Это **не испытания при реальном отключении питания**. Нет произвольного SQL в языке, проверенной матрицы Windows/macOS/Linux, безопасного публичного сервера, автоматических миграций и оснований объявлять хранилище промышленным.

[Протокол испытаний A6](https://github.com/VasiliiBabkin/sedrava/blob/main/evidence/native-server/2026-11-23-a6-sqlite.md) · [Задача #84](https://github.com/VasiliiBabkin/sedrava/issues/84) · [Проект SedravaSQL](/ru/sedravasql/)
