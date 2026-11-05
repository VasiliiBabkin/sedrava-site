---
title: Начало работы
description: Установка стабильной Sedrava 0.11.0 из PyPI и создание первого приложения.
---

Sedrava **0.11.0** — актуальный [стабильный релиз GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) и [пакет PyPI](https://pypi.org/project/sedrava/0.11.0/). В этой версии появились адаптивные сайты и интерактивные WebApp. Язык остаётся экспериментальным и не сертифицирован для промышленной эксплуатации. Прежняя стабильная [0.10.0](https://pypi.org/project/sedrava/0.10.0/) ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0)) сохранена.

## Требования

Python **3.10+**. Git нужен только для получения примеров из репозитория. Сам интерпретатор не требует сторонних Python-библиотек.

## Установка опубликованной версии

~~~sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install sedrava==0.11.0
sedrava --version
~~~

Ожидаемая версия — `0.11.0`. Для разработки из исходников клонируйте [репозиторий](https://github.com/VasiliiBabkin/sedrava) и выполните там `python -m pip install .`.

## Исторический кандидат 0.11.0rc1

Экспериментальная [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) опубликована на [PyPI](https://pypi.org/project/sedrava/0.11.0rc1/). Для генерации сайтов и WebApp установите именно этот кандидат в отдельном виртуальном окружении:

~~~sh
python -m pip install sedrava==0.11.0rc1
sedrava --version
~~~

Кандидат сохранён для повторяемых испытаний. Новые проекты рекомендуется начинать со [стабильной 0.11.0](https://pypi.org/project/sedrava/0.11.0/). Ни один из этих выпусков не включает встроенную базу данных или автоматические миграции. [Подробности](/ru/releases/).

## Первая программа

Сохраните UTF-8 файл **hello.sdr**:

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

Откройте **http://localhost:8000**. Интерпретатор выведет `{"count": 2}`. HTML-приложение не нуждается в отдельном серверном API.

## Создание Android-проекта

~~~sh
sedrava build android hello.sdr --output build/hello-android
~~~

Создаются исходники Android/Compose, **не APK**. Для сборки понадобятся JDK 17, Android SDK 35 и Gradle 8.11.1; см. [руководство](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

## Что дальше

[Возможности языка](/ru/language-overview/), [строки](/ru/text-010/), [примеры](/ru/examples/), [дорожная карта](/ru/roadmap/). Основная [документация 0.10](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/README.ru.md) и [ограничения](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md).

**Важно:** генерация сайтов и WebApp доступна в [стабильной 0.11.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0), но отсутствует в 0.10.0; она впервые появилась в исторической [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1). Сайт документации по-прежнему собирается с помощью Astro/Starlight.
