---
title: Getting started
description: Install the Rust CLI.
---

**Sedrava 0.12.0-alpha.2** is the current Rust toolchain. Experimental alpha, not production-ready. [Downloads](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2).

Download archive, SHA256SUMS, manifest.json, installer and RELEASE_NOTES.md together. No Python or Rust required for the executable. The installer refuses overwrite.

~~~sh
sha256sum -c SHA256SUMS
ARCHIVE=sedrava-0.12.0-alpha.2-x86_64-unknown-linux-gnu.tar.gz
HASH=$(sha256sum "$ARCHIVE" | cut -d ' ' -f 1)
sh install_native_preview.sh "$ARCHIVE" "$HASH" "$HOME/.local/sedrava/0.12.0-alpha.2"
export PATH="$HOME/.local/sedrava/0.12.0-alpha.2/bin:$PATH"
sedrava --version
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
