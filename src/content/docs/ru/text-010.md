---
title: Текстовые значения (разработка 0.10)
description: Полноценные Unicode-строки в неопубликованной разработке Sedrava 0.10.
---

> **Функция в разработке:** реализована в исходниках 0.10.0.dev0, но отсутствует в опубликованной 0.9.0a1. Это ещё не полноценный выпуск 0.10.

В Sedrava появились неизменяемые текстовые состояния, производные логические значения, точное сравнение строк, типизированный ввод, локальное сохранение и атомарные действия. Возможности реализованы для Python CLI и генераторов Web и Android/Compose.

## Работающий пример

```text
app "Text profile"
state name = "Guest"
persist name
derive named = name != ""
action rename: name = "Алиса 😀"
rule named
test rename: rename -> name == "Алиса 😀"
screen main:
    input name
    value name
    show named : text "Name accepted"
    button "Rename" -> rename
```

Полный пример [text_profile.sdr](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr) показывает также смешанные изменения состояния, отклонённое действие и сброс.

## Точная семантика

- Строки заключаются в двойные кавычки. Допустимы только пять escape-последовательностей: обратная косая черта, кавычка, перевод строки, возврат каретки и табуляция. Остальные отклоняются.
- Максимум **1024 скалярных значения Unicode**. Эмодзи 😀 считается одним значением; комбинируемые знаки учитываются отдельно. Непарные суррогаты запрещены.
- `==` и `!=` сравнивают точные последовательности Unicode. Нет автоматической нормализации, удаления пробелов, изменения регистра и усечения.
- Пока отсутствуют конкатенация, интерполяция, индексация, регулярные выражения, упорядочивание, преобразования и оператор длины строки.
- Некорректный черновик ввода можно исправить, не меняя принятого состояния. Правила защищают атомарные изменения. Сохраняются только поля `persist`, локально и без шифрования.
- HTML textarea может нормализовать CR/CRLF черновика в LF; сам runtime не нормализует принятые значения.

## Проверка из исходников

```sh
python -m pip install .
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/text-web/index.html
python -m http.server 8000 --directory build/text-web
```

Подробности: [справочник текста 0.10](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md) и [отчёт испытаний](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/TEXT_010_REPORT.md). Сборки APK, JVM-тесты и Lint прошли, но **интерфейс на устройстве и поворот экрана не проверялись**.
