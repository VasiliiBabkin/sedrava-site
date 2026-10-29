---
title: Examples
description: Working examples from the Sedrava source repository.
---

The language repository contains complete, executable programs for the current alpha.

## Reference application: goal and progress

The [Sedrava 0.9 Lab](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/reference_09.sdr) demonstrates integer input, derived values, rules, persistence, embedded tests and conditional text.

~~~sh
sedrava check examples/reference_09.sdr
sedrava test examples/reference_09.sdr
sedrava run examples/reference_09.sdr add add
sedrava build web examples/reference_09.sdr --output build/web/index.html
~~~

To preview the generated page:

~~~sh
python -m http.server 8000 --directory build/web
~~~

## Other programs

See [the complete example index](https://github.com/VasiliiBabkin/sedrava/blob/main/examples/README.md) for:

- A constrained counter.
- A **manual** countdown (no real-time timer in 0.9).
- Habit progress with locally persisted accepted state.
- Validated numeric input.

Examples are intended for learning and conformance checks, **not as production templates**. Android generation produces project sources. Compiling and testing an APK is a separate step.

[Install Sedrava from source](/getting-started/) before running these commands.
