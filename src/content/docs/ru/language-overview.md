---
title: Возможности языка
description: Состояния, строки, записи, действия и навигация в опубликованной Sedrava 0.10.0.
---

[**Sedrava 0.10.0**](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) доступна на [PyPI](https://pypi.org/project/sedrava/0.10.0/). Язык экспериментальный: версия 0.10.0 ещё не гарантирует совместимости со всеми последующими изменениями.

## Состояния и текст

Файлы имеют расширение `.sdr`, ключевые слова записываются по-английски. Поддерживаются знаковые int32, логические значения, точный текст Unicode, типизированные записи и ограниченные упорядоченные коллекции.

~~~text
state goal = 5
state progress = 0
state note = "One thing at a time"
derive reached = progress >= goal
~~~

Сохраняемые состояния отмечаются словом `persist`. Строки ограничены **1024 скалярными значениями Unicode**; автоматической нормализации и обрезки пробелов нет. [Подробнее о тексте](/ru/text-010/).

## Атомарные действия и правила

Действие изменяет кандидатное состояние. Переполнение, нарушение типов или итоговых правил приводит к отказу от всего действия.

~~~text
action add:
    if progress < goal:
        progress = progress + 1
rule goal >= 1 and goal <= 20
rule progress >= 0 and progress <= goal
~~~

Принятое состояние при отказе не меняется частично.

## Записи, коллекции и экраны

В 0.10.0 есть типизированные записи, списки до **100** элементов с устойчивыми ID и навигация между экранами со стеком до **32** элементов. Интерфейс включает текст, значения, поля ввода, кнопки, списки и переходы с условиями. [Пример менеджера задач](/ru/examples/).

~~~text
test once: add -> progress == 1
screen main:
    text "Progress"
    value progress
    value reached
    button "Add" -> add
~~~

## Команды

| Команда | Назначение |
| --- | --- |
| `sedrava check FILE` | Проверка синтаксиса, типов, начальных ограничений |
| `sedrava test FILE` | Запуск встроенных тестов |
| `sedrava run FILE ACTION...` | Выполнение действий, вывод JSON |
| `sedrava build web FILE --output PATH` | Генерация автономного HTML |
| `sedrava build android FILE --output DIR` | Генерация исходников Kotlin/Compose |

Сборка APK выполняется отдельно. Экспериментальная команда `build site` для адаптивных сайтов разрабатывается в [черновом PR №22](https://github.com/VasiliiBabkin/sedrava/pull/22) и **не входит в 0.10.0**.

## Ограничения

Нет автоматических миграций, зашифрованного хранения, настоящих таймеров, произвольной вёрстки, модулей, асинхронных сервисов и гарантий API 1.0. [Ограничения](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md), [совместимость](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/COMPATIBILITY_010.md), [справочник текста 0.10](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md). Проверка конечного APK 0.10 на физическом телефоне пока не подтверждена.
