---
title: Benchmarks
description: Comparative VDS measurements, 24 November 2026.
---

Two runs on Linux x86_64, two Skylake vCPUs and 7941 MiB RAM. Sedrava 6883818 and SedravaSQL c086094, **before the HTTP wait optimization**. Internal experiment, not independent audit.

| Scenario | Sedrava | Baseline |
| --- | ---: | ---: |
| Source check | 3.89 ms | Python Sedrava 211.22 ms |
| 5000 actions | 22.01 ms | Python Sedrava 557.50; Rust 5.41 ms |
| Peak RSS, 5000 actions | 5.63 MiB | Python Sedrava 22.25 MiB |
| Journal source | 2949 bytes | TypeScript/HTML/CSS 6278 |
| Journal build | 10.75 ms | tsc 8224.26 ms |
| Journal DOM | 416.54 ms | TypeScript 214.77 ms |
| INSERT | 1.313 ms | SQLite 1.453 ms |
| Aggregate | 0.756 ms | SQLite 0.074 ms |
| HTTP 1 client | 99 req/s | FastAPI 277; Express 197 |
| HTTP 8 clients | 733 req/s | FastAPI 426; Express 453 |
| Android debug APK | 8.773 MB | Kotlin 8.707 MB |

CLI includes process startup; DOM uses jsdom, not a real browser; tsc is nonincremental; SQLite and NativeLog differ in receipt/history semantics. HTTP tests are short loopback series and competitors use SQLite. Android build is not device execution. All 120 transaction workflows passed, not proof of production reliability. Human productivity was not measured.

[Methodology and raw results](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BENCHMARK_2026_11_24.ru.md) · [SQL](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/BENCHMARK_2026_11_24.ru.md)


Earlier measurements on this page are the pre-B26–B28 baseline; they do not measure A30. **A30 release (28 November 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) and [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. A single verified Linux x86-64 package with three CLIs: [downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [distribution guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 passed VDS release qualification; earlier A26 passed independent Forgejo CI. COW B32–B36 remains research. Not production-ready.
