---
title: SedravaSQL
description: Experimental SQLite-backed managed API and independent Rust SQL engine.
---

[SedravaSQL](https://github.com/VasiliiBabkin/sedravasql) is an Apache-2.0 project in the Sedrava ecosystem, dedicated to the memory of Dmitry Grabylnikov.

Two experimental engines: managed SQLite key/value API with CAS, audit and durable receipts; independent NativeLog SQL B23 with typed tables, SELECT/INSERT/UPDATE/DELETE, joins, aggregates, GROUP BY/HAVING, DISTINCT, secondary indexes, foreign keys and bounded sequential transactions. B24/B25 provides separate mutable pages, redo WAL, cache and B+Tree splits. SQL still uses the journal, not B25. No full SQL server, production guarantee or valuable data.

~~~sh
git clone https://github.com/VasiliiBabkin/sedravasql.git
cd sedravasql
cargo build --locked --release
cargo build --locked --release --manifest-path native-engine/Cargo.toml
~~~

[Official site and downloads](https://sql.virtreal.ru/) · [SQL B23](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_SQL_B23.ru.md) · [B25](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/NATIVE_TREE_B25.ru.md) · [Benchmarks](/benchmarks/)
