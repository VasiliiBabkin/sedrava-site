---
title: Releases and previews
description: Published Sedrava version and explicitly unpublished 0.11 and 0.12 development tracks.
---

## Published version: Sedrava 0.10.0

Sedrava **0.10.0** was released on 31 October 2026: [GitHub release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) · [PyPI package](https://pypi.org/project/sedrava/0.10.0/). This is the latest verified public stable-version identifier in the project. It supports typed text, records, bounded collections and checked multi-screen navigation on existing application targets.

## 0.11.0rc1 — preparing a release candidate, NOT published

[Candidate preparation PR #42](https://github.com/VasiliiBabkin/sedrava/pull/42) is open and contains a source version bump, read-only CI gates and bilingual release notes. **No `v0.11.0rc1` GitHub release or PyPI package is asserted here.** Do not install it by an unverified package version.

The planned candidate focuses on what the experimental Web integration actually implements: `build site`, `build webapp`, typed reusable components, functions, bounded collection operations, forms, routes and guarded public HTTP clients. Four source examples are under test. The existing Web/Android application targets remain supported in the candidate code.

Read the [English](https://github.com/VasiliiBabkin/sedrava/blob/release/011-rc1-preparation/docs/RELEASE_NOTES_0_11_0rc1.en.md) or [Russian](https://github.com/VasiliiBabkin/sedrava/blob/release/011-rc1-preparation/docs/RELEASE_NOTES_0_11_0rc1.ru.md) draft notes and [release gates](https://github.com/VasiliiBabkin/sedrava/blob/release/011-rc1-preparation/docs/RELEASE_TRACK_011.md).

## 0.12.0a1 — proposed experimental alpha, NOT published

The following changes are implemented on **unmerged experimental branches**, not in published Sedrava: [namespaced modules PR #39](https://github.com/VasiliiBabkin/sedrava/pull/39), [original-file diagnostics PR #40](https://github.com/VasiliiBabkin/sedrava/pull/40), and [offline local packages/lockfile PR #41](https://github.com/VasiliiBabkin/sedrava/pull/41). Version `0.12.0a1` is a release plan, not an available download. The experimental modules still use lexical lowering rather than complete typed-IR symbol identity, and the package system has no online registry.

## Explicit boundaries

No released or candidate version currently provides a trusted Sedrava-generated backend, SQLite/PostgreSQL database, authentication or multi-user authorization. Browser HTTP requests are clients of an independently operated service, not a built-in server.

This production documentation site is built with **Astro/Starlight**. Separately, the team maintains a [Sedrava-authored development preview](https://dev.virtreal.ru/) and the [`sedrava-site` repository](https://github.com/VasiliiBabkin/sedrava-site). These are distinct build tracks.
