---
title: Платформа A30
description: Experimental integrated platform and offline distribution.
---

Скачайте [готовый комплект](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) и следуйте [инструкции установки](/ru/getting-started/). Для сборки из исходников используйте проверенный тег. Только тестовые данные.

**Выпуск A30 (28 ноября 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) и [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. Единый проверенный комплект Linux x86-64 из трёх CLI: [загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [установка](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 прошёл приёмку на VDS; ранее A26 прошёл независимый Forgejo CI. COW B32–B36 остаётся исследованием. Не для production.

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
git checkout --detach 761213bfd0240ffc6a2390045c125def4b87e194
cargo build --manifest-path rust/Cargo.toml --locked --release --bin sedrava
export PATH="$PWD/rust/target/release:$PATH"
~~~

Создание проекта, сборка, проверка и упаковка:

~~~sh
sedrava new myapp
cd myapp
sedrava test
sedrava build
sedrava package --output ../myapp-preview
sedrava project verify-package ../myapp-preview
~~~

Создайте приватный каталог данных с правами 0700. Файл авторизации подготовьте по [руководству A23d](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/SERVER_SESSIONS_A23D.ru.md). 

~~~sh
DATA="$HOME/myapp-data"
mkdir -m 700 "$DATA"
# Prepare the auth file before serving.
sedrava migrate --data "$DATA" --trusted --apply
sedrava serve --data "$DATA" --auth-file "$DATA/auth.json" --trusted --allow-write --port 8080
~~~

Сервер только loopback, не публикуйте в интернет. Миграции добавочные, база привязана к имени проекта. A30: 6 097 061 байт, три CLI. Проверки: 85 Rust, 319 HTTP, 21+73 SQL, 23 HTTP из установленного комплекта, jsdom, шесть негативных сценариев установщика. Linux x86-64 GNU, Ubuntu 24.04. Не production.
