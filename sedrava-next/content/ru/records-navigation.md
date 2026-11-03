## Записи и ограниченные списки

Опубликованная 0.10.0 поддерживает именованные скалярные поля и упорядоченные коллекции вместимостью 1–100. Фрагмент объявления:

```sdr
record Task:
    title: text
    done: bool
state tasks: list<Task>(max=100) = []
state selected = 0
persist tasks
```

Операции: append/has/get/update/remove/count/next_id. Положительный ID не зависит от позиции и не используется повторно. Ошибка вместимости/типа/int32 откатывает всё действие; инварианты проверяются до принятия. Неявных преобразований нет.

## Несколько экранов

Опубликованный app-режим объявляет screen и явный блок navigation. Стек push/pop ограничен 32 переходами; переход может включать атомарное действие. Состояние общее. Guards обрабатывают отсутствие выбранной записи без непроверенного индексирования.

Полные источники: [менеджер задач](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager_navigation.sdr), [контракт записей](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/RECORDS_COLLECTIONS_010.md), [навигация](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/NAVIGATION_010_CONTRACT.md).

## Экспериментальный WebApp

[Живой пример задач](/ru/examples/#tasks) использует view/hash routes, шаблоны строк и запросы ядра из экспериментальной 0.11. Это отдельный UI-синтаксис, не опубликованный screen 0.10. Проверяемое состояние и атомарность сохраняются.
