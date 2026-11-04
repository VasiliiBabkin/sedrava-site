# Native Sedrava documentation preview

**Work in progress; no production replacement or release.** Website branch `feature/sedrava-native-docs-live-examples`, draft [site PR #10](https://github.com/VasiliiBabkin/sedrava-site/pull/10). Compiler [PR #36](https://github.com/VasiliiBabkin/sedrava/pull/36), separate native-docs extension [PR #37](https://github.com/VasiliiBabkin/sedrava/pull/37). Exact SHA in `compiler.json` and the read-only preview workflow.

## Source and build

`site.sdr` declares every page, layout, locale link, native documentation component and live demo. `components/chrome.sdr` contains reusable navigation/footer/sidebar. Source-controlled Markdown is content, not an Astro wrapper. No generated HTML/CSS/JS is manually changed. Build orchestration only creates explicit provenance Markdown input before invoking standard `sedrava check` and `sedrava build site`; the compiler builds the four declared WebApps and preserves their standalone bytes.

```sh
# Obtain the compiler at the exact commit in compiler.json in a separate checkout.
python -m pip install '/path/to/compiler[docs]' playwright==1.62.0
python sedrava-next/build.py --compiler /path/to/compiler
python sedrava-next/check_preview.py
python -m http.server 8000 --directory build/native-site
```

`build/native-site/` is the complete static tree (30 site pages + 4 demo routes). `native-provenance.json` records actual website/compiler SHA, dirty-tree status, dependency versions and file hashes. Each demo has exact downloadable `.sdr`, source SHA and generated-file hashes in `docs-demos.json`. Local fonts include the Inter OFL notice. `migrate_content.py --check` proves all 12 original canonical pages and their fenced source are preserved under the reviewed transformation; the production `src/content/docs` is not modified.

## Implemented and under acceptance

- Bilingual homepages explicitly say “This website is built with Sedrava” / “Этот сайт написан на Sedrava”. Stable 0.10.0 and experimental 0.11 are distinguished.
- All original routes plus bilingual CLI/records/navigation/releases/compatibility/project/preview/provenance pages, shared responsive disclosure sidebar, current-section links, previous/next and heading TOC.
- Checked local Markdown (raw HTML rejected by the compiler), syntax-highlighted source with copy/download, local offline full-text search across both languages with keyboard and safe excerpts.
- Inline counter, tasks, CRM and typed HTTP catalog, each compiled from the same file shown next to the running iframe. Reload and individual reset retain unrelated storage.
- Trusted author demos share the site's origin; they are **not an untrusted-code sandbox**. No arbitrary editor, raw script or secret API key.
- The HTTP catalog is explicitly **CI-endpoint-only**. The browser acceptance server supplies real HTTP; a plain static host reports an honest 404/error, not synthetic live data.

## Checks

```sh
npm install --prefix build/a11y --no-audit --no-fund axe-core@4.10.3
python -m playwright install chromium
python sedrava-next/test_browser.py
```

The preview workflow uploads separate site, screenshot/result and trace artifacts for each engine. It tests Chromium/Firefox/WebKit, 320/360/390/768/1024/1440 widths, source/download parity, actions/persistence/reset, offline Cyrillic/English search, real HTTP methods/errors and axe. Static parity currently verifies **12 retained routes, 30 native pages, four compiled demos, eight exact source panels, 1047 local links/resources**. Latest local Chromium acceptance: **8/8 passed** on the pinned compiler, including the complete reference pages and local font faces. The compiler full suite passed **272 tests**; its pinned SHA passed native-docs Chromium/Firefox/WebKit and packaging CI; longer Android/integration jobs are tracked separately. Website cross-engine CI for the next published checkpoint remains pending. Independent standard `build webapp` runs match the embedded bytes for all four demos. CI links/counts will be added after actual runs on the published SHA.

## Staging and production

Current Astro production and `sedrava-dev` deployment are untouched. This workflow uploads artifacts only. Do not merge to main, create a release/tag, publish a package or replace `sedrava.virtreal.ru`. Dev publication must be separately gated, target only the already documented approved dev directory/domain, and be verified remotely before a staging GO is claimed. Until acceptance and remote checks finish: **NO-GO for production**, staging artifacts under review.

## Resume

Run `check_preview.py`, then the browser suite; fix real failures without loosening requirements. Keep both compiler pins synchronized. Finish cross-engine/visual review, immutable provenance/CI evidence and the gated staging/rollback instructions before proposing any publication.
