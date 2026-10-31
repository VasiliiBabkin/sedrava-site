---
title: Roadmap
description: Published Sedrava 0.10.0 and the next experimental language milestones.
---

Sedrava [0.10.0](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) was publicly released on 31 October 2026 and is available on [PyPI](https://pypi.org/project/sedrava/0.10.0/). Numbered future milestones are development plans, not release dates or promises.

| Stage | Focus | Status |
| --- | --- | --- |
| **0.9** | Core state/actions, checked arithmetic and Web/Android generation | Historical GitHub alpha |
| **0.10** | Unicode text, typed records, bounded lists, multi-screen navigation | **Published** on GitHub and PyPI |
| **0.11** | Responsive Web UI and website generation | **Draft PR #22**, not included in 0.10.0 |
| **0.12+** | Device capabilities, reusable modules, editor support and hardening | Proposed, not scheduled |
| **1.0** | Versioned specification and compatibility commitments | Long-term objective |

## Current work

A [0.11 Web UI development branch](https://github.com/VasiliiBabkin/sedrava/pull/22) explores static website generation from `.sdr`, with responsive components, themes and asset checks. **It is not released** and should not be confused with this official documentation website, which is independently built with Astro/Starlight in [sedrava-site](https://github.com/VasiliiBabkin/sedrava-site).

## Project principles

- Express application behavior, typed state and invariants rather than platform boilerplate.
- Preserve validated semantics between Python, generated Web and Android.
- Prioritize explicit limits and local/offline operation where possible.
- Keep experimental features separate from published releases.
- Report validation limits, including unverified device configurations.

Source of truth: [language roadmap](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/ROADMAP.md), [known limitations](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/KNOWN_LIMITATIONS.md). Features may change as development progresses.
