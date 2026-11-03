Code less boilerplate. Express more intent.

## State. Actions. Rules. An application.

Sedrava is an experimental declarative programming language. Describe the behavior of a small application once, then generate a standalone Web app or an Android/Jetpack Compose project.

## One source, shared behavior

01 / DECLARE

### Describe state

Define integers, booleans, text, typed records, bounded collections, derived values and UI without platform setup.

02 / PROTECT

### Enforce invariants

Actions are atomic: rejected final states and arithmetic failures never partially change accepted state.

03 / GENERATE

### Build two targets

Create a self-contained Web page or native Android project with multi-screen navigation from the same program.

## A small Sedrava program


~~~text title="hello.sdr"
app "Hello Sedrava"
state count = 0
action add: count = count + 1
rule count >= 0 and count <= 10
test once: add -> count == 1
screen main:
    text "Hello Sedrava"
    value count
    button "Add" -> add
~~~


Use `sedrava check` to validate, `sedrava test` to run embedded tests and `sedrava build web` or `sedrava build android` to generate a target.

**Sedrava 0.10.0 · Published on GitHub and PyPI**

Released 31 October 2026. Text, typed records, bounded collections and multi-screen navigation are available. This is an experimental language release, not production certification. Final 0.10 physical Android acceptance is not yet documented. [Release notes](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) · [Install from PyPI](https://pypi.org/project/sedrava/0.10.0/).

## Dedicated to a teacher

Sedrava is dedicated to **Gennady Ivanovich Smirnykh**, the computer science teacher who helped its creator understand and love programming. Read the [bilingual dedication](https://github.com/VasiliiBabkin/sedrava/blob/main/DEDICATION.md). This tribute does not imply participation or endorsement.

## Explore Sedrava

[Install Sedrava 0.10.0](/getting-started/)
[Browse examples](/examples/)
[Language overview](/language-overview/)
[Roadmap](/roadmap/)
[Source on GitHub](https://github.com/VasiliiBabkin/sedrava)
