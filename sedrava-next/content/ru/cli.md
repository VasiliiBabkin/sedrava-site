## Команды опубликованной 0.10.0

| Команда | Результат |
|---|---|
| `sedrava --version` | Версия компилятора |
| `sedrava check FILE` | Синтаксис, типы, начальные ограничения |
| `sedrava test FILE` | Встроенные тесты |
| `sedrava run FILE ACTION...` | Принятое состояние JSON |
| `sedrava build web FILE --output FILE` | Автономный Web HTML |
| `sedrava build android FILE --output DIR` | Исходники Android/Compose |

```sh
python -m pip install sedrava==0.10.0
sedrava check examples/task_manager_navigation.sdr
sedrava test examples/task_manager_navigation.sdr
sedrava build web examples/task_manager_navigation.sdr --output build/web/index.html
python -m http.server 8000 --directory build/web
```

## Сборка Android

Генерация не является сборкой APK: нужны JDK 17, Android SDK 35 и Gradle 8.11.1. Для обновления сохраняйте application ID и ключ подписи. [Руководство](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

## Экспериментальные Web targets

`build site` и `build webapp` относятся к экспериментальной 0.11, а не опубликованной 0.10.0. [Происхождение сборки](/ru/provenance/) фиксирует SHA компилятора. Устанавливайте его с extras docs в отдельное окружение, не подменяя опубликованную версию незаметно.
