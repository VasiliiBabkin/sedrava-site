---
title: Roadmap
description: Published Sedrava 0.10.0 and verified experimental 0.11/0.12 development.
---

Sedrava **0.11.0** is published as the [latest stable release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) ([PyPI](https://pypi.org/project/sedrava/0.11.0/)); [0.10.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) remains available as the previous stable version. The 0.11.0rc1 experimental candidate is historical; 0.12 and later stages are not yet released.

| Stage | Focus | Status |
| --- | --- | --- |
| **0.10.0** | Text, records, collections, multi-screen applications | Previous stable release |
| **0.11.0rc1** | Responsive sites, interactive WebApps, typed client HTTP | **Published experimental prerelease** ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) · [PyPI](https://pypi.org/project/sedrava/0.11.0rc1/)) |
| **0.11.0** | Reviewed Web platform | **Published stable** ([GitHub](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) · [PyPI](https://pypi.org/project/sedrava/0.11.0/)) |
| **0.12.0a1** | Aliased namespaces, source diagnostics, offline local dependency locking | Implemented experimental stacked [PR #39–41](https://github.com/VasiliiBabkin/sedrava/pull/41), alpha not published |
| **0.13+** | Trusted server target, SQLite then authentication/migrations | Architecture proposal, not implemented |
| **1.0** | Frozen specification, supported APIs and compatibility rules | Long-term objective |

## Current work

The candidate is based on [Web platform integration PR #36](https://github.com/VasiliiBabkin/sedrava/pull/36). Namespaces and packages are separate experimental work. Details and current availability are on the [release status page](/releases/).

The official documentation site still uses **Astro/Starlight**; the [Sedrava-authored development preview](https://dev.virtreal.ru/) is separate. Server-side authentication, SQLite and a package registry must not be described as released capabilities.
## Project principles

- Express application behavior, typed state and invariants rather than platform boilerplate.
- Preserve validated semantics between Python, generated Web and Android.
- Prioritize explicit limits and local/offline operation where possible.
- Keep experimental features separate from published releases.
- Report validation limits, including unverified device configurations.

Source of truth: [language roadmap](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/ROADMAP.md), [known limitations](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md). Features may change as development progresses.
