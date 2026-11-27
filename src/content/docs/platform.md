---
title: A28 platform
description: Experimental integrated platform and offline distribution.
---

Verified candidate, not a public alpha release. Build from the exact A26 commit and use disposable data. The previously published 0.12.0-alpha.2 does not include these new commands.

**A28 development candidate (27 November 2026).** A26 integration passed both Forgejo jobs; A28 offline Linux x86-64 package and installation passed. Published alpha archives are unchanged. NativeLog remains the SQL backend; B32–B36 COW research is not adopted. See [platform distribution](https://github.com/VasiliiBabkin/sedrava/blob/feat/a28-distribution/docs/PLATFORM_DISTRIBUTION_A28.ru.md) and [integration evidence](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/INTEGRATION_A26.ru.md).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
git checkout --detach f688f992f0e6e047b03ffdb968ddd4a454b091fe
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

Loopback server only; do not expose to the Internet. Additive migrations, project-name binding. A28: 4,732,501 bytes, two CLIs; archive verified but not publicly released. Qualification: 85 Rust, 319 HTTP, 21+73 SQL tests, 23 installed-binary HTTP requests and jsdom. Not production-ready.
