---
title: Начало работы
description: Установка Sedrava из GitHub и создание первого веб-приложения.
---

Sedrava 0.9.0a1 — **опубликованная экспериментальная альфа-версия на GitHub**. Пакета Sedrava на PyPI пока нет. Текущие исходники содержат также **неопубликованное текстовое ядро 0.10.0.dev0**; см. [справочник](/ru/text-010/).

## Что потребуется

Python **3.10 или новее** и Git. Для работы интерпретатора не требуются сторонние Python-зависимости.

## Установка из исходников

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
python -m venv .venv
~~~

Активируйте виртуальное окружение:

- Linux/macOS: **. .venv/bin/activate**
- Windows PowerShell: **.venv\Scripts\Activate.ps1**

Установите проект:

~~~sh
python -m pip install .
sedrava --version
sedrava --help
~~~

## Первая программа

Создайте UTF-8 файл **hello.sdr**:

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

Проверьте программу и создайте веб-приложение:

~~~sh
sedrava check hello.sdr
sedrava test hello.sdr
sedrava run hello.sdr add add
sedrava build web hello.sdr --output build/web/index.html
python -m http.server 8000 --directory build/web
~~~

Откройте **http://localhost:8000**. Команда run выводит **{"count": 2}** в формате JSON. Сгенерированная веб-страница содержит код приложения и не требует отдельного сервера приложения.

## Создание Android-проекта

~~~sh
sedrava build android hello.sdr --output build/hello-android
~~~

Команда создаёт **исходники Android/Compose, а не готовый APK**. Для сборки APK дополнительно понадобятся JDK, Android SDK и Gradle. Точные версии указаны в [руководстве по сборке](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

## Дальше

Изучите [возможности языка](/ru/language-overview/), [примеры](/ru/examples/) и [планы развития](/ru/roadmap/). [Полный справочник синтаксиса 0.9](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_9.md) — основной источник по семантике альфа-версии.
