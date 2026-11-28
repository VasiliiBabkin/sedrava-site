---
title: Getting started
description: Install the Rust CLI.
---

**Sedrava 0.12.0-alpha.3** is the current Rust toolchain. Experimental alpha, not production-ready. [Downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3).

Download all seven files from the versioned download page into one directory. The installer checks SHA-256 and refuses to overwrite an existing prefix. No Python or Rust required on PATH.

~~~sh
sha256sum -c SHA256SUMS
ARCHIVE=sedrava-sedrava-platform-0.12.0-alpha.3-sql-0.1.0-alpha.2-linux-x86_64.tar.gz
HASH=438d8a974bd9edf3247da25d28fa76a96ad5e33a5d17554b3eec62b22a2f934f
sh install_platform_a30.sh "$ARCHIVE" "$HASH" "$HOME/sedrava-alpha3"
export PATH="$HOME/sedrava-alpha3/bin:$PATH"
sedrava --version
sedravasql --version
sedravasql-native-preview --version
~~~

## First program

Save as hello.sdr (UTF-8).

~~~text
app "Hello Sedrava"
state count = 0
action add: count = count + 1
rule count >= 0 and count <= 10
test once: add -> count == 1
screen main:
    text "Hello Sedrava"
    value count
    button "Add" -> add
~~~

~~~sh
sedrava check hello.sdr
sedrava test hello.sdr
sedrava run hello.sdr add add
sedrava build web hello.sdr --output build/hello.html
sedrava build android hello.sdr --output build/hello-android --application-id org.example.hello
~~~

Android generates source; APK builds require JDK/SDK/Gradle. [Build](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md) · [Examples](/examples/).

The project CLI is included in alpha.3. [A30 platform](/platform/).
