---
title: SedravaSQL
description: Experimental SQLite-backed managed API and independent Rust SQL engine.
---

**A28 development candidate (27 November 2026).** A26 integration passed both Forgejo jobs; A28 offline Linux x86-64 package and installation passed. Published alpha archives are unchanged. NativeLog remains the SQL backend; B32–B36 COW research is not adopted. See [platform distribution](https://github.com/VasiliiBabkin/sedrava/blob/feat/a28-distribution/docs/PLATFORM_DISTRIBUTION_A28.ru.md) and [integration evidence](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/INTEGRATION_A26.ru.md).

[A24 migration contract](https://github.com/VasiliiBabkin/sedravasql/blob/integration/a26-platform/docs/NATIVE_MIGRATIONS_A24.ru.md) · [Platform](/platform/)

[SedravaSQL](https://github.com/VasiliiBabkin/sedravasql) is an Apache-2.0 project in the Sedrava ecosystem, dedicated to the memory of Dmitry Grabylnikov.

Two experimental engines: managed SQLite key/value API with CAS, audit and durable receipts; independent NativeLog SQL B28 in main with typed tables, SELECT/INSERT/UPDATE/DELETE, joins, aggregates, GROUP BY/HAVING, DISTINCT, secondary indexes, foreign keys and bounded sequential transactions. B24/B25 provides separate mutable pages, redo WAL, cache and B+Tree splits. SQL still uses the journal, not B25. No full SQL server, production guarantee or valuable data.

~~~sh
git clone https://github.com/VasiliiBabkin/sedravasql.git
cd sedravasql
cargo build --locked --release
cargo build --locked --release --manifest-path native-engine/Cargo.toml
~~~

[Official site and downloads](https://sql.virtreal.ru/) · [SQL B23](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B23.ru.md) · [B25](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_TREE_B25.ru.md) · [Benchmarks](/benchmarks/)

## Historical B31 checkpoint (24–25 November 2026)

**Public releases remain unchanged:** [Sedrava 0.12.0-alpha.2](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2) and [SedravaSQL 0.1.0-alpha.1](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.1), Linux x86-64 GNU. Rust is the sole maintained Sedrava implementation. Neither release is production-ready.

| Track | Verified source basis | Status |
|---|---|---|
| Sedrava main | [896685c](https://github.com/VasiliiBabkin/sedrava/commit/896685ce31f915d1ab69223f98451c2504792cf7) | 83 Rust tests, 63 HTTP A17–A21 requests |
| SedravaSQL main | [363ccbc](https://github.com/VasiliiBabkin/sedravasql/commit/363ccbc9542ed8e3ecf41e3619f78823ffeb97d4) | NativeLog SQL B28, 67 tests, strict Clippy |
| Storage research | [a98e709](https://github.com/VasiliiBabkin/sedravasql/commit/a98e709cc591057298818d0972c12cf020054295) | B31, 81 tests, strict Clippy; not the SQL backend |

B26 reuses validated schemas; B27 directly decodes JSON scalars (row cache rejected); B28 bounds primary-key range reads in the in-memory ordered Replay. In the 2048-key paired experiment, 1/8/32-row ranges were 138.4×/89.7×/37.8× faster than forced full scans with a redundant predicate. Disk-tree projection B28-A was not adopted.

B29 implements a separate binary copy-on-write B+Tree, 4 KiB pages, 64-node cache, up to 16 distinct mutations per atomic batch. B30 builds independent compact copies preserving revisions, generation and tombstones (20,480 keys; final phase 50.79 to 10.94 MB). B31 adds checksummed overflow chains for UTF-8 text up to 64 KiB, inline up to 256 bytes (960 keys, 16.08 MB payload, 24.76 to 18.87 MB after compaction). Compact-copy materialized payload budget is 32 MiB, verified at the exact boundary and one byte over.

Measurements are workload-specific on a shared VDS, not universal speedups or proof of superiority over SQLite. Process-exit tests do not establish physical power-loss durability. These post-release changes are not in the public archives. Milestone IDs are not release versions.

Historical next steps; see the A28 update above.

**Reports and raw evidence:** [B26](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B26_PERFORMANCE.ru.md) · [B27](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B27_PERFORMANCE.ru.md) · [B28](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B28_ORDERED_RANGE.ru.md) · [B28-A](https://github.com/VasiliiBabkin/sedravasql/blob/research/b28-tree-sql/docs/NATIVE_SQL_B28_TREE_EXPERIMENT.ru.md) · [B29](https://github.com/VasiliiBabkin/sedravasql/blob/research/b29-cow-tree/docs/NATIVE_COW_B29.ru.md) · [B30](https://github.com/VasiliiBabkin/sedravasql/blob/research/b30-compact/docs/NATIVE_COW_B30.ru.md) · [B31](https://github.com/VasiliiBabkin/sedravasql/blob/research/b31-overflow/docs/NATIVE_COW_B31.ru.md).
