---
title: Sedrava Native — Rust
description: Native alpha compiler, Web/Android and local SQL API A21.
---

**Sedrava Native 0.12.0-alpha.1** is a standalone experimental Rust toolchain. The sedrava-native command does not replace stable Python 0.11.0 ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0), [PyPI](https://pypi.org/project/sedrava/0.11.0/)). For development and learning, not production.

## Installation

Linux x86_64: [native archives and SHA-256](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.1/). The installed binary needs neither Python nor Rust. Windows/macOS builds are not verified.

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava-native
./rust/target/release/sedrava-native --version
./rust/target/release/sedrava-native check examples/service_journal.sdr
./rust/target/release/sedrava-native build webapp examples/service_journal.sdr --output build/journal
~~~

## Verified scope

- State, records, bounded collections, functions, navigation, Unicode, checking and execution.
- Site/WebApp and Kotlin/Compose generators; Android debug APK build verified, not the full device matrix.
- Trusted Host with bounded file effects.
- Local HTTP A1–A16; separate database-api A17–A21 with named parameters, Bearer roles, SQL queries, bounded transactions and durable receipts.
- Self-host A5.11b: separate experimental compiler written in Sedrava with functions and nested if/while, not the main compiler.

Loopback only, one writer, bounded resources. No public service or valuable data. Complete Python parity, real-browser tests, Windows/macOS and production security are not established.

[Distribution](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/DISTRIBUTION_NATIVE.ru.md) · [SQL API A21](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/SALES_DEMO_A21.ru.md) · [SedravaSQL](/sedravasql/) · [Benchmarks](/benchmarks/)
