---
title: Text values (0.10 development)
description: First-class Unicode text in the unreleased Sedrava 0.10 development increment.
---

> **Development feature:** Implemented in source at 0.10.0.dev0, not part of the published 0.9.0a1 release. Not a completed 0.10 release.

Sedrava now supports immutable text state, text-derived booleans, exact equality, typed input, local persistence, and atomic actions across the Python CLI, generated Web apps, and Android/Compose sources.

## Working example

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

The complete [text_profile.sdr](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr) also demonstrates mixed state updates, rejected actions and reset.

## Exact semantics

- Double-quoted text literals support only `\\`, `\"`, `\n`, `\r`, and `\t` escapes. Invalid escapes are rejected.
- Maximum length: **1024 Unicode scalar values**. Emoji such as 😀 count as one scalar; combining marks count individually. Unpaired surrogates are invalid.
- Equality and inequality (`==`, `!=`) compare exact scalar sequences. No normalization, trimming, case folding or truncation.
- No concatenation, interpolation, indexing, regex, ordering, conversion or text-length operator yet.
- Invalid editor drafts remain editable without changing accepted state. Rules protect atomic changes. Only declared `persist` fields are stored locally, without encryption.
- HTML textarea may normalize CR/CRLF in a draft to LF; accepted model values are not normalized by the runtime.

## Try from source

```sh
python -m pip install .
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/text-web/index.html
python -m http.server 8000 --directory build/text-web
```

For complete grammar, Android instructions, compatibility notes and test evidence, see the [authoritative 0.10 text reference](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md) and [engineering report](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/TEXT_010_REPORT.md). Android APK build, JVM and Lint checks passed; device UI and rotation were **not** verified.
