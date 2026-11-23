---
title: Native Rust (experimental)
description: Build Sedrava's experimental standalone Rust compiler and loopback-only server without replacing stable 0.11.0.
---

Sedrava has an independently developed **native Rust implementation** in the [main repository](https://github.com/VasiliiBabkin/sedrava). It covers a growing, tested subset of language, Web, Android, Host and server functionality. It is **experimental**, not a new stable release or a complete compatibility replacement for the published Python-based **0.11.0**.

**Published release:** [0.11.0 on GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) and [PyPI](https://pypi.org/project/sedrava/0.11.0/). Historical [0.10.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) ([PyPI](https://pypi.org/project/sedrava/0.10.0/)) and [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) ([PyPI](https://pypi.org/project/sedrava/0.11.0rc1/)) remain available. Experimental 0.12.0a1 is not a published stable release.

## Build a native preview from source

On an environment with a compatible Rust toolchain and Cargo:

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
cargo build --manifest-path rust/Cargo.toml --locked --bin sedrava-native
cargo test --manifest-path rust/Cargo.toml --locked --all-targets
./rust/target/debug/sedrava-native server check examples/native_server/sqlite_a5.sdr
~~~

The binary is built from the repository. **Do not install the Python PyPI package expecting that it contains the A6 Rust server.** Rust runtime operations do not require Python, though development verification scripts may use Python. Availability and validation differ by OS; the A6 evidence is for Ubuntu Linux x86_64.

## Server progression

| Mode | Experimentally implemented | Boundaries |
| --- | --- | --- |
| A1–A2 | Strict local HTTP, typed server state and guarded snapshots | Localhost only; not a public API |
| A3 | Request keys, CAS revisions and atomic state snapshots | 32 permanent receipts; hard cap |
| A4 | Bounded fsynced redo journal | No checkpoint or production power-loss proof |
| A5 | SedravaSQL-backed SQLite state, atomic audit and response ledger | Still 32 embedded application receipts |
| **A6** | Separate immutable SQL receipts; no 32-entry cap; first read-only database expression | No automatic receipt retention, write DSL or public authentication |

A6 uses a *new opt-in storage mode* and **does not silently migrate A5 files**. The only current direct database expression in a Sedrava server is a checked literal read in a GET response:

~~~text
server "A6 SQL Read Example"
state enabled: bool = true
route GET "/note":
    respond 200 { note: db_get("public_notes/welcome"), enabled: state.enabled }
~~~

The example requires an existing private SedravaSQL SQLite database and the experimental flag shown in the [Server A6 documentation](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/RUST_NATIVE_SERVER_A6_SQLITE.ru.md). It is **not** an online, publicly exposed interactive database playground. The expression cannot execute arbitrary SQL, write records, or access the server's reserved internal namespace.

## Evidence and remaining work

The integration evidence records **78 Rust tests**, live local HTTP tests beyond the 32-receipt threshold, exact replay after restart, and four *debug-only* forced process exits around the SQLite commit boundary. These are **not physical power-loss tests**. There is no demonstrated general SQL DSL, cross-platform distribution matrix, secure public service, automatic schema migration or production-grade storage.

[Reproducible A6 test report](https://github.com/VasiliiBabkin/sedrava/blob/main/evidence/native-server/2026-11-23-a6-sqlite.md) · [Open storage tracking issue #84](https://github.com/VasiliiBabkin/sedrava/issues/84) · [SedravaSQL project](/sedravasql/)
