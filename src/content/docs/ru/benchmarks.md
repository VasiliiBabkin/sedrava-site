---
title: Измерения производительности
description: Сравнительные испытания VDS от 24 ноября 2026 года.
---

Два прогона на Linux x86_64, 2 vCPU Intel Xeon Skylake, 7941 МиБ RAM. Измерена сборка 6883818 Sedrava и c086094 SedravaSQL, **до оптимизации HTTP ожидания**. Это внутренний эксперимент, не независимый аудит.

| Сценарий | Sedrava | Сравнение |
| --- | ---: | ---: |
| Проверка исходника | 3,89 мс | Python Sedrava 211,22 мс |
| 5000 действий | 22,01 мс | Python Sedrava 557,50; Rust 5,41 мс |
| Пиковый RSS 5000 действий | 5,63 МиБ | Python Sedrava 22,25 МиБ |
| Журнал: исходники | 2949 байт | TypeScript/HTML/CSS 6278 |
| Журнал: сборка | 10,75 мс | tsc 8224,26 мс |
| Журнал: DOM | 416,54 мс | TypeScript 214,77 мс |
| INSERT | 1,313 мс | SQLite 1,453 мс |
| Агрегация | 0,756 мс | SQLite 0,074 мс |
| HTTP 1 клиент | 99 req/s | FastAPI 277; Express 197 |
| HTTP 8 клиентов | 733 req/s | FastAPI 426; Express 453 |
| Android debug APK | 8,773 МБ | Kotlin 8,707 МБ |

CLI включает запуск процесса; DOM — jsdom, не браузер; tsc без incremental; SQL сравнивает синхронную запись и квитанции с неодинаковой семантикой; HTTP короткие локальные серии, SQLite у конкурентов. Android — сборка, не скорость исполнения. 120 транзакционных бизнес-сценариев завершились без ошибок, но это не доказательство надёжности в production. Нет измерения труда человека.

[Подробная методика и первичные данные](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BENCHMARK_2026_11_24.ru.md) · [SQL](https://github.com/VasiliiBabkin/sedravasql/blob/main/docs/BENCHMARK_2026_11_24.ru.md)


Прежние измерения на этой странице — базовая серия до B26–B28, а не измерения A30. **Выпуск A30 (28 ноября 2026).** [Sedrava 0.12.0-alpha.3](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.12.0-alpha.3) и [SedravaSQL 0.1.0-alpha.2](https://github.com/VasiliiBabkin/sedravasql/releases/tag/v0.1.0-alpha.2), NativeLog 0.0.2. Единый проверенный комплект Linux x86-64 из трёх CLI: [загрузки](https://sedrava.virtreal.ru/downloads/0.12.0-alpha.3/) · [установка](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PLATFORM_RELEASE_A30.ru.md). A30 прошёл приёмку на VDS; ранее A26 прошёл независимый Forgejo CI. COW B32–B36 остаётся исследованием. Не для production.
