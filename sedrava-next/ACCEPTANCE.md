# Native site acceptance evidence / Проверка нативного сайта

Status: implementation and final cross-engine verification in progress. No production replacement, package publication, release or tag. See the draft [website PR #10](https://github.com/VasiliiBabkin/sedrava-site/pull/10) and separate [compiler PR #37](https://github.com/VasiliiBabkin/sedrava/pull/37), based on [#36](https://github.com/VasiliiBabkin/sedrava/pull/36).

## Actual implementation

- Source-authored `site.sdr` and reusable `.sdr` chrome; no Astro wrapper or generated-output patch.
- All **12 original routes** retained; reviewed MDX-to-Markdown migration preserves every original fenced example byte-for-byte, including indentation. Only obsolete Astro/preview implementation wording changes in the migrated copies; production sources remain unchanged.
- **30 native pages**: bilingual original docs plus records/navigation, CLI, releases, compatibility, dedication/project, complete Web-platform reference and native-site authoring. Complete compiler references have source/target hashes and immutable compiler attribution.
- Four actual embedded WebApps (counter/tasks/CRM/catalog), eight exact source panels across EN/RU, downloadable source, syntax highlighting, accessible line gutters, copy, reload and individually scoped reset. Independent standard `build webapp` outputs match every embedded app file.
- Local full-text search includes both languages, actual document text/headings/code, case folding, excerpts, no-results and keyboard handling. No runtime search request or remote dependency.
- Checked Markdown/URLs/assets, self-only scripts/frames, no raw HTML/eval/editor, explicit same-origin author trust, real child initialization/error state. HTTP catalog is **CI endpoint only** until an approved actual server exists on staging.
- Own source-controlled amethyst/gold/ivory presentation, actual local Latin/Cyrillic font faces and weights, MIT/Apache/OFL notices, responsive sidebar/TOC/current/previous/next/locale navigation, SEO/sitemap/robots and immutable build provenance.

## Measured checkpoints

Compiler `6b0d9a9be455699482749e139fb2407b5827fd11` passed its applicable CI, including [native docs engines](https://github.com/VasiliiBabkin/sedrava/actions/runs/41732703752), [full Python/package matrix](https://github.com/VasiliiBabkin/sedrava/actions/runs/41732703770), [records Android](https://github.com/VasiliiBabkin/sedrava/actions/runs/41732703748) and [navigation Android](https://github.com/VasiliiBabkin/sedrava/actions/runs/41732703666). These links are explicitly an earlier checkpoint, not proof of later compiler commits.

Local subsequent runs: **272 full compiler Python tests**, four dedicated docs unit cases, one actual compiler embed/search/history browser scenario, and five pre-existing standalone WebApp collection browser cases passed at their recorded checkpoints. Dedicated compiler browser invocation also discovers the four unit cases (five tests total); it is not four browser scenarios.

The native website's **eight local Chromium scenarios** passed with the full references and final typography (51.321 seconds). They verify counter persistence and copy, task CRUD/search/filter/routes/delete, CRM relations/forms/dialog/theme/reset isolation, real HTTP methods/schema/errors/retry/cancel/404, offline bilingual search, source downloads, six widths and representative axe checks. Four local staging-safety unit cases pass; these are not remote-deployment tests.

The first website cross-engine run on `373c3a6` passed Chromium but failed Firefox/WebKit: the tests incorrectly rejected legitimate cached `304` navigations, and WebKit exposed joint iframe history interference. The response check now verifies the actual rendered title/h1 for 200/304. The compiler now gives embeds a bounded owned route trail, preserving the parent/sibling history and standalone behavior. These corrections must pass final hosted runs; earlier failures are not hidden.

## Defects found and corrected

| Issue | Correction and regression evidence |
|---|---|
| Compiler SHA was overwritten by an independent-demo hash dictionary in provenance | Separate variables; static acceptance now checks exact compiler/website SHA and all output hashes |
| MDX conversion stripped indentation inside complete examples | Preserve fences separately; migration checker compares every original fence |
| Reload reset the selected detail route | Child reload preserves current URL/hash; real browser route/state assertion |
| Sticky parent navigation obscured a child modal | Trusted lifecycle observer centers the frame on modal open and is disposed/reconnected |
| Mobile-closed sidebar could stay inaccessible after widening | MatchMedia lifecycle sync; resize with a closed disclosure is checked |
| Sibling iframe history interfered with in-app Back, especially WebKit | Frame-owned trail/replace semantics; parent Back remains document navigation |
| Browser history rejection could commit a navigation action too early | History acceptance precedes data/view commit; failure-injection regression retains state |
| Missing child script could be labelled merely “loaded” | Runtime readiness marker and real missing-resource browser regression |
| Source line numbers could pollute copy/hash | Separate aria-hidden unselectable gutter; exact source/download checks |
| One Latin font face was advertised as arbitrary weights | Actual local 400/600/700 Latin/Cyrillic faces; browser decoding is checked |
| Off-screen skip link appeared in element screenshot clips | Standard clipped hidden state, preserved keyboard reveal/activation |

## Evidence layout and final SHA

Each successful CI engine artifact contains:

- `native-site/`: the complete static tree, four apps and downloadable exact sources;
- `native-independent/`: standard CLI comparison outputs;
- `native-parity.json`: measured page/route/link/source counts;
- `native-provenance.json`: **actual checkout SHA**, dirty flag, immutable compiler SHA, versions, all artifact hashes;
- `native-browser-evidence/`: real results, toolchain, API calls, axe output, screenshots at 320/360/390/768/1024/1440 and per-scenario Playwright traces.

The final SHA is generated in CI rather than self-referencing this document. The PR is updated with actual final run/artifact links after completion. Do not substitute a previous green run for the latest commit.

## Decisions and remaining external gates

**Artifact inspection:** GO only when the final SHA passes all three engines, parity and independent-build checks.

**Verified dev deployment:** NO-GO until a real explicitly dispatched staging run backs up the approved dev tree and passes actual remote byte/route/cache checks. The session's public dev connection is blocked by the network proxy (`403 CONNECT`); no remote checks or SSH execution are claimed. Backup directory/SSH configuration is not assumed. See [staging contract](STAGING.md).

**Production cutover:** NO-GO without remote acceptance and a separate explicit owner decision. `main` still deploys Astro; neither its workflow nor production content has been changed. Staging extraction is not atomic, catalog has no staging API, and same-origin demos are not isolated untrusted programs. These limits are explicit.

Русский: источник истины итогового SHA и результатов — манифесты CI и PR, не предыдущий зелёный запуск. Официальный production не менялся. Артефакты можно принять только после финальной матрицы; реальный dev и откат не проверены из-за сетевого 403. Для production требуется отдельное решение владельца.
