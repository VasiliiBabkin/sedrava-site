---
title: Roadmap
description: The planned stages of Sedrava development.
---

Sedrava is developed incrementally. Version numbers below are planning milestones, **not release dates or promises**.

| Stage | Focus | Status |
| --- | --- | --- |
| **0.9** | State, actions, invariants, tests, basic Web/Android generators | Published GitHub alpha |
| **0.10** | Text input, richer UI, themes, navigation, multi-screen app | Text core implemented in unreleased source; remaining UI planned |
| **0.11** | Collections, records and migration strategy | Planned; text core moved forward to 0.10 |
| **0.12–0.13** | Device capabilities, modules, reusable components | Planned |
| **0.14–0.15** | Editor integration and desktop target | Planned |
| **0.16–0.19** | Hardening, security, accessibility and compatibility | Planned |
| **1.0** | Versioned specification and stability policy | Long-term goal |

## Project principles

- Describe application behavior instead of writing platform boilerplate.
- Preserve the semantics of actions and invariants between targets.
- Prefer offline-first applications where possible.
- Declare capabilities and persistence explicitly.
- Separate tested code from released software.

A visual builder and additional platforms are longer-term possibilities. AI-assisted tooling may be added later, but the language runtime should remain usable without AI.

The source repository has the authoritative [roadmap](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/ROADMAP.md). Feature status may change as development progresses.

Contributions and issue reports are welcome on [GitHub](https://github.com/VasiliiBabkin/sedrava/issues).
