---
title: Текстовые значения (0.10.0)
description: Unicode-строки в опубликованной Sedrava 0.10.0.
---

> **Опубликовано в 0.10.0:** [PyPI](https://pypi.org/project/sedrava/0.10.0/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0). Язык остаётся экспериментальным.

Sedrava поддерживает неизменяемые текстовые состояния, вычисляемые логические значения, точное Unicode-сравнение, типизированный ввод, локальное сохранение и атомарные действия для Python CLI, Web и Android/Compose.

## Пример

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

Полный [text_profile.sdr](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr).

## Точная семантика

- Строки в двойных кавычках. Допустимы escape-последовательности для обратной косой черты, кавычек, `\n`, `\r`, `\t`; остальные отклоняются.
- Максимум **1024 скалярных значения Unicode**. 😀 считается одним, комбинируемые символы — по отдельности. Непарные суррогаты недопустимы.
- `==` и `!=` сравнивают точные последовательности: без нормализации, обрезки пробелов, изменения регистра и усечения.
- Отсутствуют конкатенация, интерполяция, индексация, регулярные выражения, упорядочивание, оператор длины и преобразование в целое.
- Некорректный черновик не изменяет принятое состояние. Только поля `persist` хранятся локально, без шифрования.
- HTML textarea может нормализовать CR/CRLF черновика; принятые моделью строки не меняются автоматически.

## Проверка версии из PyPI

```sh
python -m pip install sedrava==0.10.0
# В клоне репозитория языка:
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/text-web/index.html
python -m http.server 8000 --directory build/text-web
```

Подробности: [справочник текста](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md), [отчёт испытаний](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/TEXT_010_REPORT.md) и [статус испытаний телефона](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PHYSICAL_DEVICE_010.md). Эмуляторные проверки выполнены, полноценный протокол приёмки конечного APK 0.10 на устройстве не подтверждён.
