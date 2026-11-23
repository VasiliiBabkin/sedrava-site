---
title: SedravaSQL
description: Experimental open-source Rust and SQLite-backed transactional database from the Sedrava ecosystem.
---

**SedravaSQL** is a separate public [Apache-2.0 project](https://github.com/VasiliiBabkin/sedravasql) in the Sedrava ecosystem. It is dedicated to the memory of **Dmitry Grabyl'nikov**.

It currently ships an **experimental Rust library and CLI built on SQLite**, not a replacement for PostgreSQL, a network SQL server or a production-ready general-purpose database. The software has a small bounded key/value interface with a versioned schema and auditable mutations.

## What works today

| Capability | Verified scope |
| --- | --- |
| Embedded Rust + SQLite | WAL and FULL synchronous mode; bounded key/value records |
| Change workflow | Plan/preview, per-key revision CAS, PUT/GET/LIST/DELETE |
| Atomicity | A managed value, audit record and request receipt commit together |
| Idempotency | Request keys and stored application responses; exact replay |
| Backup | SQLite online Backup API, integrity and schema checks |
| Security boundary | Owner-only new database files on Unix; refuses symlink and extra hardlink |
| Sedrava integration | Experimental native Server A5/A6; direct read-only db_get in A6 |

These are scoped implementation claims, **not guarantees of crash-proof storage**, isolation from malicious users with the same OS identity or security certification.

## Build and try it locally

From a Rust development environment:

~~~sh
git clone https://github.com/VasiliiBabkin/sedravasql.git
cd sedravasql
cargo build --locked
cargo test --locked --all-targets
python3 scripts/verify_local.py
~~~

Example with disposable local data (choose a private directory, never overwrite a database you need):

~~~sh
mkdir -m 700 -p /tmp/sedravasql-example
DB=/tmp/sedravasql-example/data.sqlite
BIN=./target/debug/sedravasql
"$BIN" init "$DB"
"$BIN" put "$DB" example welcome "Hello from SedravaSQL" --expect 0 --request-key example-request-0001
"$BIN" get "$DB" example welcome
"$BIN" verify "$DB"
"$BIN" backup "$DB" /tmp/sedravasql-example/backup.sqlite
~~~

## Architecture and development

SedravaSQL's Rust API now also supports atomically storing an optional bounded JSON application response together with the mutation receipt; these records are **not automatically deleted**. The native [Sedrava A6](/rust-native/) server uses that feature for replayable HTTP operations. There is no database write operator in the Sedrava language yet.

**Outstanding:** typed multi-key transactions, schema migrations, resource quotas, receipt retention/archiving, cross-platform verification, physical power-loss tests, authentication and public deployment. The database is not appropriate for valuable production records.

[Source and quick start](https://github.com/VasiliiBabkin/sedravasql) · [Implemented scope](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/IMPLEMENTED_V0_1.ru.md) · [Verification](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/VERIFICATION.md) · [Roadmap](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/ROADMAP.md)
