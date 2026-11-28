---
title: Sedrava on Rust
description: Primary language implementation.
---

**Sedrava 0.12.0-alpha.3** is the current Rust toolchain. Experimental alpha, not production-ready. [Downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
./rust/target/release/sedrava --version
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
~~~

Typed state, records, bounded collections, functions, navigation, Unicode, imports and locks. Web/Site/WebApp, Kotlin/Compose, trusted Host and local SQL API A21 with roles and bounded transactions. Self-host A5.11b is a separate experiment. B25 is not yet the SQL backend.

Linux x86-64 GNU tested on Ubuntu 24.04. Windows/macOS, full browser/device coverage, legacy compatibility and production security are not established. Generator support varies by target. Loopback only; disposable test data.

[Distribution](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md) · [SQL](/sedravasql/) · [Benchmarks](/benchmarks/).


**A30 release (28 November 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) and [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. A single verified Linux x86-64 package with three CLIs: [downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [distribution guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 passed VDS release qualification; earlier A26 passed independent Forgejo CI. COW B32–B36 remains research. Not production-ready.

The project CLI is included in alpha.3. [A30 platform](/platform/).
