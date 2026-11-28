---
title: Sedrava на Rust
description: Основная реализация языка.
---

**Sedrava 0.12.0-alpha.3** — текущая линия, основная реализация на Rust. Экспериментальная alpha, не для production. [Загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
./rust/target/release/sedrava --version
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
~~~

Типизированное состояние, записи, ограниченные коллекции, функции, навигация, Unicode, импорты и локальные пакеты. Web/Site/WebApp, Kotlin/Compose, trusted Host, локальный HTTP и SQL API A21 с ролями и ограниченными транзакциями. Self-host A5.11b — отдельный эксперимент. B25 пока не backend SQL.

Проверено Linux x86-64 GNU на Ubuntu 24.04. Windows/macOS, полный набор браузеров и устройств, совместимость старых проектов и промышленная безопасность не доказаны. Не все конструкции поддерживаются всеми генераторами. Сервер только loopback; тестовые данные.

[Distribution](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md) · [SQL](/ru/sedravasql/) · [Benchmarks](/ru/benchmarks/).


**Выпуск A30 (28 ноября 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) и [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. Единый проверенный комплект Linux x86-64 из трёх CLI: [загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [установка](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 прошёл приёмку на VDS; ранее A26 прошёл независимый Forgejo CI. COW B32–B36 остаётся исследованием. Не для production.

Проектный CLI доступен в alpha.3. [Платформа A30](/ru/platform/).
