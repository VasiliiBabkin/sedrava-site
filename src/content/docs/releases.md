---
title: Releases and previews
description: Published Sedrava version and published 0.11.0rc1 candidate and unpublished 0.12 experiments.
---

## Previous stable: Sedrava 0.10.0

Sedrava **0.10.0** was released on 31 October 2026: [GitHub release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) · [PyPI package](https://pypi.org/project/sedrava/0.10.0/). This is the previous stable version. It supports typed text, records, bounded collections and checked multi-screen navigation on existing application targets.

## 0.11.0rc1 — published experimental prerelease

[GitHub Pre-release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) · [PyPI package](https://pypi.org/project/sedrava/0.11.0rc1/).

Sedrava **0.11.0rc1** is published from audited commit 6051310a2ba2d542966588f12e0360c3f7c2a4d9. The GitHub and PyPI publication workflows completed successfully. This is an **experimental release candidate, not stable 0.11.0**.

To install in a separate virtual environment:

~~~sh
python -m pip install sedrava==0.11.0rc1
sedrava --version
~~~

The prerelease adds responsive site generation (build site), interactive browser applications (build webapp), typed reusable components and pure functions, bounded collection queries, forms, tables, dialogs, routes and validated public HTTP clients. Previous Web/Android application targets are retained. Source examples: [site, tasks, catalog, CRM](https://github.com/VasiliiBabkin/sedrava/tree/v0.11.0rc1/examples).

Independent checks covered actual 0.10.0 to 0.11.0rc1 upgrade and rollback, browser storage in Chromium/Firefox/WebKit and an Android API35 debug upgrade. See the [verified audit](https://github.com/VasiliiBabkin/sedrava/blob/v0.11.0rc1/docs/UPGRADE_AUDIT_011.md).

Limitations: no built-in trusted backend, SQLite/PostgreSQL, authentication, multiuser authorization, automatic schema migrations, namespaced packages or physical-device certification. A browser HTTP client needs a separately provided server. Production Android downgrade is not guaranteed.

## Latest stable: Sedrava 0.11.0

[GitHub stable release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0) · [PyPI 0.11.0](https://pypi.org/project/sedrava/0.11.0/).

**0.11.0** is the published stable release following the independently tested 0.11.0rc1. Its reviewed source is commit `c9cde75e3d2e2c7eafeeaec10c73fec627816e68`; Android versionCode is `11002`, above the RC `11001`.

Install in a dedicated Python virtual environment:

~~~sh
python -m pip install sedrava==0.11.0
sedrava --version
~~~

Includes responsive multi-page sites (`build site`), interactive browser WebApps (`build webapp`), typed components, pure functions, bounded collections, forms, dialogs, tables, routes, and checked public HTTP GET/POST/PUT/PATCH/DELETE clients. Four sample sources: site, tasks, catalog and CRM. Previous 0.10 application, Web and Android targets remain supported.

The [stable acceptance contract](https://github.com/VasiliiBabkin/sedrava/blob/v0.11.0/docs/STABLE_RELEASE_GATES_011.md) covers actual 0.10 → 0.11 → 0.10 and 0.11rc1 → 0.11 → RC in-place Python installs, Chromium/Firefox/WebKit and Android API35 debug update. This is **not** production certification. No generated trusted backend, SQLite/PostgreSQL, authentication, multiuser authorization, schema migrations, physical Android-device certification or production Android downgrade support is supplied. Namespaces and packages remain experimental 0.12 development.

## 0.12.0a1 — proposed experimental alpha, NOT published

The following changes are implemented on **unmerged experimental branches**, not in published Sedrava: [namespaced modules PR #39](https://github.com/VasiliiBabkin/sedrava/pull/39), [original-file diagnostics PR #40](https://github.com/VasiliiBabkin/sedrava/pull/40), and [offline local packages/lockfile PR #41](https://github.com/VasiliiBabkin/sedrava/pull/41). Version `0.12.0a1` is a release plan, not an available download. The experimental modules still use lexical lowering rather than complete typed-IR symbol identity, and the package system has no online registry.

## Explicit boundaries

No released or candidate version currently provides a trusted Sedrava-generated backend, SQLite/PostgreSQL database, authentication or multi-user authorization. Browser HTTP requests are clients of an independently operated service, not a built-in server.

This production documentation site is built with **Astro/Starlight**. Separately, the team maintains a [Sedrava-authored development preview](https://dev.virtreal.ru/) and the [`sedrava-site` repository](https://github.com/VasiliiBabkin/sedrava-site). These are distinct build tracks.
