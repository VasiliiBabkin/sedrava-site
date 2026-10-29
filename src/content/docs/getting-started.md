---
title: Getting started
description: Install Sedrava from GitHub and generate a first Web application.
---

Sedrava 0.9.0a1 is a **published experimental GitHub alpha**. Sedrava is not published on PyPI. The source checkout currently contains additional **unreleased 0.10.0.dev0 text support**; see the [text reference](/text-010/).

## Requirements

You need Python **3.10 or later** and Git. The language interpreter has no runtime third-party dependencies.

## Install from source

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
python -m venv .venv
~~~

Activate your virtual environment:

- Linux/macOS: **. .venv/bin/activate**
- Windows PowerShell: **.venv\Scripts\Activate.ps1**

Then install from the checkout:

~~~sh
python -m pip install .
sedrava --version
sedrava --help
~~~

## Write your first program

Create a UTF-8 file called **hello.sdr**:

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

Run checks and generate a Web app:

~~~sh
sedrava check hello.sdr
sedrava test hello.sdr
sedrava run hello.sdr add add
sedrava build web hello.sdr --output build/web/index.html
python -m http.server 8000 --directory build/web
~~~

Open **http://localhost:8000**. The run command prints **{"count": 2}** as deterministic JSON. The generated Web page contains its application logic and does not require an application server.

## Generate Android sources

~~~sh
sedrava build android hello.sdr --output build/hello-android
~~~

This generates an Android/Compose project, **not an APK**. Compiling an APK also requires JDK, Android SDK and Gradle. See the [upstream Android build guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md) for verified versions.

## Next steps

Read the [language overview](/language-overview/), [examples](/examples/) and [roadmap](/roadmap/). The [full 0.9 language reference](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_9.md) is the normative source for this alpha.
