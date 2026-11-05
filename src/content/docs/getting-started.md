---
title: Getting started
description: Install stable Sedrava 0.11.0 from PyPI and build Web applications.
---

Sedrava **0.11.0** is the current [stable GitHub release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) and [PyPI package](https://pypi.org/project/sedrava/0.11.0/), with responsive sites and interactive WebApps. The language is still experimental and not production certified. Previous stable [0.10.0](https://pypi.org/project/sedrava/0.10.0/) ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0)) is retained.

## Requirements

Python **3.10+**. Git is only needed to obtain repository examples. No third-party Python runtime dependencies are required.

## Install the released package

~~~sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install sedrava==0.11.0
sedrava --version
~~~

The expected version is `0.11.0`. To develop from sources instead, clone the [repository](https://github.com/VasiliiBabkin/sedrava) and run `python -m pip install .` there.

## Historical 0.11.0rc1 prerelease

The experimental [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) is now published on [PyPI](https://pypi.org/project/sedrava/0.11.0rc1/). To try the new site and WebApp targets, install that exact version in a separate virtual environment:

~~~sh
python -m pip install sedrava==0.11.0rc1
sedrava --version
~~~

The prerelease is preserved for reproducible testing. For new projects use [stable 0.11.0](https://pypi.org/project/sedrava/0.11.0/). Neither version includes a generated database or automatic schema migration. [Release details](/releases/).

## Your first program

Save this UTF-8 file as **hello.sdr**:

~~~text title="hello.sdr"
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
sedrava build web hello.sdr --output build/web/index.html
python -m http.server 8000 --directory build/web
~~~

Open **http://localhost:8000**. The interpreter prints `{"count": 2}`. The Web output is a self-contained HTML application; it does not need a back-end server.

## Generate an Android project

~~~sh
sedrava build android hello.sdr --output build/hello-android
~~~

This generates Android/Compose sources, **not an APK**. Building an APK needs JDK 17, Android SDK 35 and Gradle 8.11.1; see the [build guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

## Next steps

Read [language overview](/language-overview/), [text semantics](/text-010/), [examples](/examples/) and [roadmap](/roadmap/). Also see [current language documentation](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/README.en.md) and [known limitations](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md).

**Important:** site and WebApp generation are available in [stable 0.11.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0); they are absent from 0.10.0 but were introduced in the historical [0.11.0rc1 prerelease](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1). The official documentation site itself still uses Astro/Starlight.
