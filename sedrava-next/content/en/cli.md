## Published 0.10.0 commands

| Command | Result |
|---|---|
| `sedrava --version` | Compiler version |
| `sedrava check FILE` | Syntax, types and initial constraints |
| `sedrava test FILE` | Embedded source tests |
| `sedrava run FILE ACTION...` | Accepted JSON state |
| `sedrava build web FILE --output FILE` | Standalone Web HTML |
| `sedrava build android FILE --output DIR` | Android/Compose sources |

```sh
python -m pip install sedrava==0.10.0
sedrava check examples/task_manager_navigation.sdr
sedrava test examples/task_manager_navigation.sdr
sedrava build web examples/task_manager_navigation.sdr --output build/web/index.html
python -m http.server 8000 --directory build/web
```

## Android compilation

Generation is not APK compilation. JDK 17, Android SDK 35 and Gradle 8.11.1 are required for APK builds. Keep a stable application ID and signing key when updating. Read the [build guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

## Experimental website targets

`build site` and `build webapp` are experimental 0.11 features, not commands in the published 0.10.0 package. This website pins the compiler commit on its [provenance page](/provenance/). Install its docs extra in an isolated environment; do not silently replace the published compiler.
