---
title: Начало работы
description: Установка Rust CLI.
---

**Sedrava 0.12.0-alpha.2** — текущая линия, основная реализация на Rust. Экспериментальная alpha, не для production. [Загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.2/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.2).

Скачайте архив, SHA256SUMS, manifest.json, установщик и RELEASE_NOTES.md в один каталог. Готовому бинарнику не нужны Python и Rust. Установщик не перезаписывает существующую команду.

~~~sh
sha256sum -c SHA256SUMS
ARCHIVE=sedrava-0.12.0-alpha.2-x86_64-unknown-linux-gnu.tar.gz
HASH=$(sha256sum "$ARCHIVE" | cut -d ' ' -f 1)
sh install_native_preview.sh "$ARCHIVE" "$HASH" "$HOME/.local/sedrava/0.12.0-alpha.2"
export PATH="$HOME/.local/sedrava/0.12.0-alpha.2/bin:$PATH"
sedrava --version
~~~

## Первая программа

Сохраните UTF-8 файл hello.sdr.

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

Android создаёт исходники; для APK нужны JDK/SDK/Gradle. [Build](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md) · [Examples](/ru/examples/).

Для новых команд проектного CLI используйте проверенный кандидат A26/A28, а не старый опубликованный архив. [Платформа A28](/ru/platform/).
