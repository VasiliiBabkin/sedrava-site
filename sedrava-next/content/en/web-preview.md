## What runs here

This website is built with Sedrava. Native site pages, Markdown, local full-text search and source-bound live WebApp demos compile through the experimental compiler in [PR #36](https://github.com/VasiliiBabkin/sedrava/pull/36) and its [docs extension #37](https://github.com/VasiliiBabkin/sedrava/pull/37). The [provenance page](/provenance/) pins actual commits. The package metadata remains the published 0.10.0 while the integration is reviewed; do not assume published 0.10 contains these features.

## Capabilities and boundaries

Responsive components, local CSS/fonts, controlled modules, pure functions, bounded collection queries, forms/tables/dialogs, hash routes and typed public HTTP are experimental. The [live examples](/examples/) are real compiled applications, not simulated widgets. The HTTP catalog is explicitly CI-endpoint-only until an approved actual server exists on staging.

Demos are trusted author code on the same origin. They are not isolated untrusted playgrounds. No source editor, arbitrary JS, secrets, CORS bypass, auth/database or secure generated backend is offered. Copy/download source, reload and per-demo reset are explicit.

## Release and deployment

No 0.11 release, package publication or production cutover. The site remains static HTML/CSS/local scripts suitable for Nginx. Dev deployment needs separate gated approval and actual directory/credentials. Do not merge the preview branch into production main.
