---
title: Платформа A28
description: Experimental integrated platform and offline distribution.
---

Проверенный кандидат, не опубликованный alpha-релиз. Сборка из точного коммита A26; используйте только отдельные тестовые данные. Публичная версия 0.12.0-alpha.2 не содержит новых команд.

**Кандидат A28 (27 ноября 2026).** Интеграция A26 прошла обе проверки Forgejo; автономный комплект Linux x86-64 A28 и его установка проверены. Публичные alpha-архивы не изменены. SQL использует NativeLog; COW B32–B36 не принят как основной движок. [Дистрибутив](https://github.com/VasiliiBabkin/sedrava/blob/feat/a28-distribution/docs/PLATFORM_DISTRIBUTION_A28.ru.md) · [Отчёт](https://github.com/VasiliiBabkin/sedrava/blob/integration/a26-platform/docs/INTEGRATION_A26.ru.md).

~~~sh
git clone https://github.com/VasiliiBabkin/sedrava.git
cd sedrava
git checkout --detach f688f992f0e6e047b03ffdb968ddd4a454b091fe
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

Сервер только loopback, не публикуйте в интернет. Миграции добавочные, база привязана к имени проекта. A28: 4 732 501 байт, два CLI; архив проверен, но ещё не опубликован. Проверки: 85 Rust, 319 HTTP, 21+73 SQL, 23 HTTP из установленного комплекта и jsdom. Не production.
