---
title: Sedrava на Rust
description: Основная реализация языка.
---

**Sedrava 0.12.0-alpha.2** — текущая линия, основная реализация на Rust. Экспериментальная alpha, не для production. [Загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
./rust/target/release/sedrava --version
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
~~~

Типизированное состояние, записи, ограниченные коллекции, функции, навигация, Unicode, импорты и локальные пакеты. Web/Site/WebApp, Kotlin/Compose, trusted Host, локальный HTTP и SQL API A21 с ролями и ограниченными транзакциями. Self-host A5.11b — отдельный эксперимент. B25 пока не backend SQL.

Проверено Linux x86-64 GNU на Ubuntu 24.04. Windows/macOS, полный набор браузеров и устройств, совместимость старых проектов и промышленная безопасность не доказаны. Не все конструкции поддерживаются всеми генераторами. Сервер только loopback; тестовые данные.

[Distribution](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/DISTRIBUTION_NATIVE.ru.md) · [SQL](/ru/sedravasql/) · [Benchmarks](/ru/benchmarks/).
