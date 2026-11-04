## Native site and documentation mode

This preview uses the experimental 0.11 compiler in PR #36 plus the optional documentation contract from PR #37. It is not included in the published 0.10.0 package. Install the exact compiler checkout with `python -m pip install '.[docs]'`: MarkdownIt 4.0.0 and Pygments 2.19.2 are build-time dependencies, not browser frameworks.

The website layout, pages, locales, components, routes and assets are authored in [site.sdr](https://github.com/VasiliiBabkin/sedrava-site/blob/feature/sedrava-native-docs-live-examples/sedrava-next/site.sdr). Source-controlled Markdown supplies content. Pages and their bundled live examples are generated directly by Sedrava without manual HTML patching.

## Local Markdown

`markdown "content/guide.md"` reads a root-contained UTF-8 file. Headings start at h2 because the containing page owns h1. Lists, tables, fenced code, emphasis, internal links and unique Unicode anchors produce checked static HTML and a table of contents. Raw HTML and Markdown image injection reject; use typed image components. Sources are bounded to 256KiB each; declared docs inputs to 4MiB and 512 dependencies; the index to 2MiB. Source/dependency hashes appear in the build manifest.

Code panels have escaped syntax highlighting for Sedrava, shell and Python, visible copy controls, exact source hashes and accessible line-number gutters. Numbers are aria-hidden and never part of copied source. No arbitrary source is executed at build time.

## Offline search and responsive navigation

`search label "Search documentation"` emits a local in-memory index of document titles, headings, body text and code in both languages. No API key, remote search request or server is needed. Latin/Cyrillic case matching, safe excerpts, empty/no-results, arrows and Escape are tested. The query is limited to 160 characters and results to 30.

`sidebar label "Documentation":` contains ordinary checked links, marks the current section and becomes a native disclosure on narrow screens. The site source composes the header/footer, locale counterpart, previous/next and sidebar rather than depending on a fixed template engine.

## Source-bound live demos

`demo "demos/counter.sdr" at "/live/counter/" label "Counter"` compiles a local WebApp under its explicitly owned route. It displays the same exact source with download/hash beside the running iframe. At most 16 trusted demos; overlapping site/demo routes and source escapes reject. The site compares embedded files to independent standard `build webapp` outputs for all four examples.

These are trusted author programs sharing the site's origin, **not isolated untrusted playgrounds**. There is no arbitrary editor, raw JS or secret. The CSP permits self scripts/frames and iframe device permissions are denied. Do not combine same-origin/script permissions and claim isolation. Any future untrusted editor requires a separate origin and explicit budgets/permissions.

Reload preserves the current frame route. Explicit reset deletes only that demo's path/name data/cache, then replaces its entry. Frame-owned Back navigation does not consume parent or sibling history. Observers are disposed on pagehide and reconnected on restoration. A missing child runtime shows an initialization failure instead of claiming a working demo.

## HTTP and deployment boundaries

The catalog requires a real declared JSON endpoint. This preview's endpoint is CI-only: static hosting shows an honest error until an approved actual service exists. Credentials/secrets/CORS bypass are not generated. All methods, schemas, cancellation, timeout and cache behavior are tested against a real loopback HTTP server.

The output is a static directory suitable for Nginx/FASTPANEL. `clean-urls true` opts into directory links, preserving previous generator defaults. Canonical/OpenGraph/sitemap are generated from the explicit dev origin; robots disables indexing. [Build provenance](/provenance/) binds actual compiler/site commits, dependency versions and file hashes. No production switch is authorized; staging needs its own accepted artifact, backup and remote checks.
