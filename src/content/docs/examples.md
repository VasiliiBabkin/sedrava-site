---
title: Examples
description: Executable examples included in Sedrava 0.10.0.
---

These examples work with the [published Sedrava 0.10.0](https://pypi.org/project/sedrava/0.10.0/) CLI. [GitHub release](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0). Clone the [language repository](https://github.com/VasiliiBabkin/sedrava) for the `examples/` source files.

## Goal and progress: historical 0.9 example

The [0.9 Lab](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/reference_09.sdr) remains a regression example for int32 input, derived values, rules and persistence.

~~~sh
sedrava check examples/reference_09.sdr
sedrava test examples/reference_09.sdr
sedrava build web examples/reference_09.sdr --output build/reference-web/index.html
~~~

## Text profile: new in 0.10

The [text profile](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/text_profile.sdr) demonstrates Unicode input, exact equality, persistence and atomic rejection.

~~~sh
sedrava check examples/text_profile.sdr
sedrava test examples/text_profile.sdr
sedrava build web examples/text_profile.sdr --output build/profile-web/index.html
~~~

See [text semantics](/text-010/).

## Task managers: records and navigation

The [single-screen task manager](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager.sdr) demonstrates typed records and bounded lists. The [two-screen task manager](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/task_manager_navigation.sdr) adds navigation and Back behavior.

~~~sh
sedrava check examples/task_manager_navigation.sdr
sedrava test examples/task_manager_navigation.sdr
sedrava build web examples/task_manager_navigation.sdr --output build/navigation-web/index.html
python -m http.server 8000 --directory build/navigation-web
~~~

Open **http://localhost:8000** to try the generated Web app. Android generation produces sources, not an APK; see the [build guide](https://github.com/VasiliiBabkin/sedrava/blob/main/docs/BUILD.md).

The [full example index](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/README.md) also includes a constrained counter, manual countdown and habit progress. Examples are for learning and conformance, not production templates.

## Four new examples in experimental 0.11.0rc1

The [published prerelease](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.11.0rc1) is available on [PyPI](https://pypi.org/project/sedrava/0.11.0rc1/). Check out the [release-tag example sources](https://github.com/VasiliiBabkin/sedrava/tree/v0.11.0rc1/examples) first, then:

~~~sh
python -m pip install sedrava==0.11.0rc1
sedrava build site examples/platform_site.sdr --output build/platform/site
sedrava build webapp examples/platform_tasks.sdr --output build/platform/tasks
sedrava build webapp examples/platform_catalog.sdr --output build/platform/catalog
sedrava build webapp examples/platform_crm.sdr --output build/platform/crm
~~~

The catalog requires an independently provided HTTP API; a static file server cannot supply that endpoint. [Read the limitations](/releases/).
