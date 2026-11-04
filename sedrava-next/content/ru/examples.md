---
title: Примеры
description: Исполняемые программы для Sedrava 0.10.0.
---

Примеры работают с [опубликованной Sedrava 0.10.0](https://pypi.org/project/sedrava/0.10.0/). [Релиз на GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0). Для файлов `examples/` клонируйте [репозиторий языка](https://github.com/VasiliiBabkin/sedrava).

## Цель и прогресс: исторический пример 0.9

[0.9 Lab](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/reference_09.sdr) — эталон для ввода чисел, вычисляемых значений, правил и сохранения.

~~~sh
sedrava check examples/reference_09.sdr
sedrava test examples/reference_09.sdr
sedrava build web examples/reference_09.sdr --output build/reference-web/index.html
~~~

## Текстовый профиль: возможности 0.10

[Текстовый профиль](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr) показывает ввод Unicode, точное сравнение строк, сохранение и атомарный отказ.

~~~sh
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/profile-web/index.html
~~~

[Справочник текстовых значений](/ru/text-010/).

## Менеджеры задач: записи и навигация

[Одноэкранный менеджер](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager.sdr) показывает записи и списки. [Двухэкранный](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager_navigation.sdr) добавляет навигацию и системную кнопку Back.

~~~sh
sedrava check examples/task_manager_navigation.sdr
sedrava test examples/task_manager_navigation.sdr
sedrava build web examples/task_manager_navigation.sdr --output build/navigation-web/index.html
python -m http.server 8000 --directory build/navigation-web
~~~

Откройте **http://localhost:8000** для просмотра Web-приложения. Android-генератор создаёт исходники, а не APK; см. [руководство по сборке](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

В [полном каталоге](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/README.md) также есть счётчик, ручной обратный отсчёт и учёт привычек. Примеры предназначены для изучения, не для промышленной эксплуатации.
