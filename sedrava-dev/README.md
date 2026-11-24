# Sedrava development showcase

Public preview: https://dev.virtreal.ru/

This static website is built from [site.sdr](site.sdr) using the current pinned Rust Sedrava generator. It is NOT the production Astro/Starlight
documentation website, nor a publicly available SQL API.

## Branding and styles

- [Official PNG master](assets/sedrava-logo-primary.png) and
  [official favicon](assets/favicon.ico) are byte-for-byte identical to
  `public/brand/sedrava-logo-primary.png` and `public/brand/favicon.ico`
  from this repository, verified by SHA-256 in `scripts/build_dev_site.py`.
- [theme.css](theme.css) is an explicit, hand-authored responsive CSS layer.
  The current experimental site generator's theme DSL covers basic color
  tokens but not all layout/typography/media-query requirements.
- The generator builds the page from the `.sdr` program. The build script
  appends the audited CSS to its generated `site.css`, inserts a CSS content
  hash into the stylesheet URL, and copies the official favicon.
- No third-party JavaScript, remote fonts, user tracking, public SQL endpoint
  or web API is deployed by this showcase.

## Verification / release

Run with an environment containing the pinned Sedrava compiler
and SEDRAVA_BIN pointing to its executable:

~~~sh
python3 scripts/build_dev_site.py
python -m pip install playwright==1.62.0
python -m playwright install chromium
python3 scripts/check_dev_responsive.py
~~~

The browser regression uses a local temporary HTTP server and checks
320/360/390/768/1280 CSS-pixel widths for horizontal overflow, loaded
logos, dark theme, accessible buttons and fatal JavaScript errors.
Screenshots are archived with the workflow artifact.

The website deploy workflow is *normally manual-only*. It requires production
SSH secrets configured in GitHub Actions. Use the approved one-off publication
mechanism rather than leaving automatic deployment enabled permanently.
