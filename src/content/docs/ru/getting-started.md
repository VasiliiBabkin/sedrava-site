---
title: Начало работы
description: Установка Rust CLI.
---

**Sedrava 0.12.0-alpha.3** — текущая линия, основная реализация на Rust. Экспериментальная alpha, не для production. [Загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3).

Скачайте все семь файлов со страницы загрузки в один каталог. Установщик проверяет SHA-256 и не перезаписывает существующий префикс. Python и Rust на PATH не требуются.

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

Проектный CLI доступен в alpha.3. [Платформа A30](/ru/platform/).
