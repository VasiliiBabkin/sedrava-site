---
title: Sedrava Native — Rust
description: Публичная alpha-линия нативного компилятора, Web/Android и локальный SQL API A21.
---

**Sedrava Native 0.12.0-alpha.1** — самостоятельный экспериментальный компилятор на Rust. Команда sedrava-native не заменяет стабильную Python 0.11.0 ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0), [PyPI](https://pypi.org/project/sedrava/0.11.0/)). Для разработки и изучения, не production.

## Установка

Linux x86_64: [нативные дистрибутивы и SHA-256](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.1/). Готовому бинарнику не нужны Python и Rust. На Windows/macOS бинарники пока не проверены.

Сборка из исходников:

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava-native
./rust/target/release/sedrava-native --version
./rust/target/release/sedrava-native check examples/service_journal.sdr
./rust/target/release/sedrava-native build webapp examples/service_journal.sdr --output build/journal
~~~

## Проверенный объём

- Состояние, записи, ограниченные коллекции, функции, навигация, Unicode, проверка и исполнение программ.
- Генерация WebApp/Site и Kotlin/Compose; сборка Android debug APK проверена, не вся матрица устройств.
- Trusted Host с ограниченными файловыми операциями.
- Локальный HTTP A1–A16; отдельный database-api A17–A21 с именованными параметрами, Bearer-ролями, SQL-запросами, ограниченными транзакциями и долговременными квитанциями.
- Self-host A5.11b: отдельный экспериментальный компилятор на Sedrava с функциями и вложенными if/while. Не основной компилятор.

Сервер только loopback, один записывающий процесс, ограниченные бюджеты. Не размещайте публично и не используйте ценные данные. Полная совместимость с Python, реальный браузер, Windows/macOS и безопасность production не доказаны.

[Документация](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/DISTRIBUTION_NATIVE.ru.md) · [SQL API A21](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/SALES_DEMO_A21.ru.md) · [SedravaSQL](/ru/sedravasql/) · [Измерения](/ru/benchmarks/)
