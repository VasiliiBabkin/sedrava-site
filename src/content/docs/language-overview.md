---
title: Language overview
description: State, atomic actions, rules, generated UI and the limitations of Sedrava 0.9.
---

Sedrava 0.9 is a deliberately small language for local applications. Its source files use the **.sdr** extension. Keywords and identifiers are written in English.

## State and derived values

The published 0.9 baseline supports **signed 32-bit integers** and **booleans**. The unreleased 0.10 source also supports **text, typed records and bounded collections**; see [text values](/text-010/). A derived value is calculated from state and cannot be assigned directly.

~~~text
state goal = 5
state progress = 0
derive reached = progress >= goal
~~~

State declarations can be marked for local persistence with the **persist** declaration.

## Atomic actions and invariants

Actions are sequential changes to a candidate state. If arithmetic overflows or a final rule is broken, the complete action is rejected without partially changing accepted state.

~~~text
action add:
    if progress < goal:
        progress = progress + 1
rule goal >= 1 and goal <= 20
rule progress >= 0 and progress <= goal
~~~

Rules apply to the final candidate state. Derived values must remain evaluable throughout each action.

## Tests and user interface

An embedded test starts from the defaults and executes its named actions independently of other tests.

~~~text
test once: add -> progress == 1
screen main:
    text "Progress"
    value progress
    value reached
    button "Add" -> add
~~~

The 0.9 UI supports literal text, displayed values, buttons, integer input and simple conditional text. The published 0.9 UI has **one screen**. Unreleased 0.10 source adds multi-screen navigation.

## Toolchain

| Command | Purpose |
| --- | --- |
| sedrava check FILE | Validate syntax, types and rules |
| sedrava test FILE | Run embedded tests |
| sedrava run FILE ACTION... | Interpret actions and print JSON state |
| sedrava build web FILE --output PATH | Generate standalone Web HTML |
| sedrava build android FILE --output DIR | Generate an Android/Compose source project |

## Important limitations

The published 0.9 alpha does **not** support text state. Text, records, collections and navigation are implemented in unreleased 0.10 source; files, asynchronous operations, automatic timers and modules remain unsupported. Web persistence uses localStorage; Android uses SharedPreferences. Neither is suitable for secrets, and migration is not supported.

Read the authoritative [0.9 language reference](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_9.md) and [known limitations](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md).
