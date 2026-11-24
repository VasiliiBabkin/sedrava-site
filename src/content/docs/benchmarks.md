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


Earlier measurements on this page are the pre-B26–B28 baseline. **B31 source checkpoint:** NativeLog B28 in main; B31 is separate research. Public alpha releases unchanged. [Status and reports](/sedravasql/).
