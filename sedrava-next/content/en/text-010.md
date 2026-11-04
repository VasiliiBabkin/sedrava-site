---
title: Text values (0.10.0)
description: First-class Unicode text in the published Sedrava 0.10.0.
---

> **Released in 0.10.0:** [PyPI](https://pypi.org/project/sedrava/0.10.0/) · [GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0). Sedrava is experimental, not a production compatibility guarantee.

Sedrava supports immutable text state, derived booleans, exact Unicode equality, typed input, local persistence and atomic actions across Python CLI, generated Web and Android/Compose.

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

See [text_profile.sdr](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr).

## Exact semantics

- Double-quoted string literals support `\\`, `\"`, `\n`, `\r` and `\t` escapes. Invalid escapes are rejected.
- Maximum **1024 Unicode scalar values**. One 😀 is one scalar; combining marks count separately. Unpaired surrogates are invalid.
- `==` and `!=` compare exact scalar sequences. No normalization, trimming, folding or truncation.
- No concatenation, interpolation, indexing, regex, ordering, text-length operator or text-to-int conversion.
- Invalid editor drafts remain editable without changing accepted state. Only explicit `persist` data is saved, without encryption.
- HTML textarea may normalize a CR/CRLF draft to LF; accepted runtime values are not normalized.

## Try the released CLI

```sh
python -m pip install sedrava==0.10.0
# In a checkout of the Sedrava repository:
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/text-web/index.html
python -m http.server 8000 --directory build/text-web
```

For grammar, limitations and measured evidence consult the [authoritative text reference](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/LANGUAGE_0_10_TEXT.md), [engineering report](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/TEXT_010_REPORT.md) and [device acceptance status](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/PHYSICAL_DEVICE_010.md). Android emulator tests were performed; full final 0.10 physical-device acceptance is not documented.
