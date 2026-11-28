---
title: A30 platform
description: Experimental integrated platform and offline distribution.
---

Download the [verified package](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) and follow [installation](/getting-started/). To build from source, use the verified commit. Disposable test data only.

**A30 release (28 November 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) and [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. A single verified Linux x86-64 package with three CLIs: [downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [distribution guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 passed VDS release qualification; earlier A26 passed independent Forgejo CI. COW B32–B36 remains research. Not production-ready.

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
git checkout --detach 761213bfd0240ffc6a2390045c125def4b87e194
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
export PATH="$PWD/rust/target/release:$PATH"
~~~

Create, build, test and package a project:

~~~sh
sedrava new myapp
cd myapp
sedrava test
sedrava build
sedrava package --output ../myapp-preview
sedrava project verify-package ../myapp-preview
~~~

Create a private data directory (0700). Prepare an authorization file following the [A23d guide](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/SERVER_SESSIONS_A23D.ru.md). 

~~~sh
DATA="$HOME/myapp-data"
mkdir -m 700 "$DATA"
# Prepare the auth file before serving.
sedrava migrate --data "$DATA" --trusted --apply
sedrava serve --data "$DATA" --auth-file "$DATA/auth.json" --trusted --allow-write --port 8080
~~~

Loopback server only; do not expose to the Internet. Additive migrations, project-name binding. A30: 6,097,061 bytes, three CLIs. Qualification: 85 Rust, 319 HTTP, 21+73 SQL tests, 23 installed-binary HTTP requests, jsdom and six negative installation cases. Linux x86-64 GNU, Ubuntu 24.04. Not production-ready.
