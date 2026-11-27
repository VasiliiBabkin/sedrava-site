---
title: Sedrava on Rust
description: Primary language implementation.
---

**Sedrava 0.12.0-alpha.2** is the current Rust toolchain. Experimental alpha, not production-ready. [Downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
./rust/target/release/sedrava --version
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
~~~

Typed state, records, bounded collections, functions, navigation, Unicode, imports and locks. Web/Site/WebApp, Kotlin/Compose, trusted Host and local SQL API A21 with roles and bounded transactions. Self-host A5.11b is a separate experiment. B25 is not yet the SQL backend.

Linux x86-64 GNU tested on Ubuntu 24.04. Windows/macOS, full browser/device coverage, legacy compatibility and production security are not established. Generator support varies by target. Loopback only; disposable test data.

[Distribution](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/DISTRIBUTION_NATIVE.ru.md) · [SQL](/sedravasql/) · [Benchmarks](/benchmarks/).


**A28 development candidate (27 November 2026).** A26 integration passed both Forgejo jobs; A28 offline Linux x86-64 package and installation passed. Published alpha archives are unchanged. NativeLog remains the SQL backend; B32–B36 COW research is not adopted. See [platform distribution](https://github.com/VasiliiBabkin/sedrava/blob/feat/a28-distribution/docs/PLATFORM_DISTRIBUTION_A28.ru.md) and [integration evidence](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/INTEGRATION_A26.ru.md).

For the new project CLI use the verified A26/A28 candidate, not the older published archive. [A28 platform](/platform/).
