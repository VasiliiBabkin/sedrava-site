---
title: Getting started
description: Install Sedrava 0.10.0 from PyPI and build your first Web application.
---

Sedrava **0.10.0** is publicly released on [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) and [PyPI](https://pypi.org/project/sedrava/0.10.0/). It remains experimental and is intended for learning and smaller local apps rather than production deployment.

## Requirements

Python **3.10+**. Git is only needed to obtain repository examples. No third-party Python runtime dependencies are required.

## Install the released package

~~~sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install sedrava==0.10.0
sedrava --version
~~~

The expected version is `0.10.0`. To develop from sources instead, clone the [repository](https://github.com/VasiliiBabkin/sedrava) and run `python -m pip install .` there.

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

**Important:** general-purpose `sedrava build site` is **not** included in 0.10.0. It is being developed in [experimental PR #22](https://github.com/VasiliiBabkin/sedrava/pull/22). This official documentation site uses Astro/Starlight separately.
