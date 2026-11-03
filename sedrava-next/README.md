# Sedrava native website: staging and interactive-documentation plan

**Branch:** feature/sedrava-native-docs-live-examples (sedrava-site).
**Status:** stage-0 working preview; **not production**. Do not publish to sedrava.virtreal.ru.
**Compiler:** experimental integration PR #36, pin exact SHA in CI. Stable published language is 0.10.0.

## Goals

Replace Astro/Starlight on the official site only after feature parity. The new site itself must compile from \`site "..." \` Sedrava source. Show a prominently visible claim in both languages: "This site is built with Sedrava" / "Этот сайт написан на Sedrava". Link to the actual site .sdr source and compiler commit. Present the release/preview distinction truthfully.

## What is committed now

- \`site.sdr\`: four real generated Sedrava pages (EN/RU home and examples) with brand styling, clear provenance, exact code snippet, source links and status caveats.
- \`demos/counter.sdr\`: small true Sedrava state/action WebApp, not a screenshot or simulated button.
- CI preview workflow builds static site plus counter, task manager and CRM WebApps from compiler PR #36. Outputs are separate managed directories; do not manually modify generated assets.
- A source consistency test checks that the two displayed counter snippets match the demo source exactly.

The site pages intentionally do **not** claim an inline running example yet: a safe same-origin or cross-origin embed of WebApp output is not currently a native Sedrava site component.

## Follow-on implementation (Codex)

1. Extend \`sedrava build site\` with an explicit, typed and tested safe \`demo\` or \`embed-webapp\` component, or a \`build project\` layout that bundles a site and explicitly listed WebApps as local routes. Prefer building real sub-apps from their original \`.sdr\` sources. Avoid arbitrary HTML injection or post-build replacement of generated HTML.
2. Embed live WebApp preview on /examples/ and /ru/examples/ with a code panel for the **same exact source**, copy button, accessible title, loading/error fallback, mobile fallback, keyboard and focus handling. Explicitly model iframe origin/sandbox/CSP; do not claim sandbox isolation with allow-scripts+allow-same-origin on the same origin.
3. Provide demos: counter, tasks, themed CRM and a typed API catalog. API demo requires an actual controlled server service or a properly labeled, deterministic fixture. Never claim public mutation endpoints are authenticated if they are not.
4. Migrate every existing English/Russian documentation page, paths, canonical metadata, release status, sidebar, code formatting and search without losing information. Add document indexing/build-time full-text search (no cloud keys); support keyboard and screen readers.
5. Keep Astro production site and existing deploy workflows unchanged until staging is reviewed and parity is independently verified. Stage in dev environment only behind explicit authorization.
6. Add CI real-browser runs of link/page/docs search and each embedded demo; check generated code matches source; verify 320/360/390/768/1024/1440 px and mobile layout, CSP, XSS, broken assets and accessibility.
7. Make native compiler dependency pinned by immutable Git commit or verified versioned artifact and keep the 0.10/0.11 release labeling truthful. Do not publish 0.11 packages automatically.

## Existing deployment constraints

Astro production site currently auto-deploys on pushes to main. The working \`dev.virtreal.ru\` workflow is opt-in for SSH publication, using Nginx and tar. Do not change or enable automatic production deploy. The old dev site has a separate \`sedrava-dev/site.sdr\` implementation.

## Acceptance

- Genuine official site entirely authored as Sedrava site source (not an Astro wrapper).
- No lost EN/RU documentation or broken old routes.
- Actual live demo code and rendered behaviour proven to come from the same source.
- Real browser tests and successful static deployment rehearsal on dev.
- Owner explicitly approves replacing production after side-by-side inspection.

## Resume

Start from this branch; examine \`sedrava-next/site.sdr\`, the preview workflow and compiler PR #36. Do the implementation, not another plan-only response. The spec intentionally separates what exists from what remains.
