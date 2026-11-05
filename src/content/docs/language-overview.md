---
title: Language overview
description: Typed language, state, Web and Android targets in stable Sedrava 0.11.0.
---

[**Sedrava 0.11.0**](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) is the current stable release on [PyPI](https://pypi.org/project/sedrava/0.11.0/); earlier [0.10.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) remains available on [PyPI](https://pypi.org/project/sedrava/0.10.0/). The language remains experimental; the stable version name does not imply a full 1.0 compatibility promise.

## State, text and derived values

Sedrava uses `.sdr` source files and English keywords. State may contain signed int32 integers, booleans, exact Unicode text, typed records and bounded ordered lists.

~~~text
state goal = 5
state progress = 0
state note = "One thing at a time"
derive reached = progress >= goal
~~~

Persistent values are explicitly declared with `persist`. Text is limited to **1024 Unicode scalars**; no automatic normalization or trimming. See [text semantics](/text-010/).

## Atomic actions and invariants

Actions change a candidate state. Checked arithmetic, type constraints, derived values and final rules determine whether the complete change is accepted.

~~~text
action add:
    if progress < goal:
        progress = progress + 1
rule goal >= 1 and goal <= 20
rule progress >= 0 and progress <= goal
~~~

A rejected action does not partially mutate the accepted domain state.

## Records, collections and screens

The published 0.10.0 implementation has typed records and ordered bounded lists (up to **100** entries), stable collection IDs and multi-screen navigation with a maximum stack depth of **32**. The UI supports text, values, input, buttons, lists and guarded screen transitions. [Task manager example](/examples/).

~~~text
test once: add -> progress == 1
screen main:
    text "Progress"
    value progress
    value reached
    button "Add" -> add
~~~

## CLI commands

| Command | Purpose |
| --- | --- |
| `sedrava check FILE` | Validate syntax, types and initial constraints |
| `sedrava test FILE` | Run embedded tests |
| `sedrava run FILE ACTION...` | Run actions, output JSON state |
| `sedrava build web FILE --output PATH` | Generate standalone HTML |
| `sedrava build android FILE --output DIR` | Generate Kotlin/Compose project sources |
| `sedrava build site FILE --output DIR` | Generate a responsive multi-page website (0.11+) |
| `sedrava build webapp FILE --output DIR` | Generate a typed interactive WebApp (0.11+) |

Android APK compilation is a separate task. Multi-page sites and interactive WebApps are available in [stable 0.11.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) ([PyPI](https://pypi.org/project/sedrava/0.11.0/)), not in 0.10.0. They first appeared in the historical [0.11.0rc1](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) ([PyPI](https://pypi.org/project/sedrava/0.11.0rc1/)). See [release details](/releases/) for HTTP client and storage limitations.

## Limitations

No automatic data migrations, encrypted persistence, trusted server/backend, user authentication, full 0.12 namespaced packages or 1.0 API stability promise. [Known limitations](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md), [compatibility](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/COMPATIBILITY_010.md), [0.10 text reference](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md). The physical-device acceptance of the final 0.10 Android APK is not yet documented.
