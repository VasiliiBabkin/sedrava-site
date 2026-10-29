---
title: Примеры
description: Рабочие примеры из репозитория Sedrava.
---

В репозитории языка есть готовые программы для текущей альфа-версии.

## Эталонное приложение: цель и прогресс

[Приложение Sedrava 0.9 Lab](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/reference_09.sdr) показывает числовой ввод, вычисляемые значения, правила, сохранение состояния, встроенные тесты и условный текст.

~~~sh
sedrava check examples/reference_09.sdr
sedrava test examples/reference_09.sdr
sedrava run examples/reference_09.sdr add add
sedrava build web examples/reference_09.sdr --output build/web/index.html
~~~

Для просмотра страницы:

~~~sh
python -m http.server 8000 --directory build/web
~~~

## Другие программы

В [полном каталоге примеров](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/README.md) доступны:

- Счётчик с ограничением значения.
- **Ручной** обратный отсчёт (настоящих таймеров в 0.9 ещё нет).
- Учёт прогресса с локальным сохранением принятого состояния.
- Ввод чисел с проверкой ограничений.

Эти примеры предназначены для изучения языка и тестирования, **не для выпуска готовых продуктов**. Android-генератор создаёт исходники; сборка и проверка APK выполняются отдельно.

Перед запуском ознакомьтесь с [инструкцией по установке](/ru/getting-started/).
