# Sedrava — official website

**https://sedrava.virtreal.ru**

The official bilingual website and documentation for [Sedrava](https://github.com/VasiliiBabkin/sedrava), an experimental declarative programming language for small Web and Android applications.

Built with Astro + Starlight. English content is published at the root; Russian translations use the /ru/ prefix.

## Development

Requires Node.js **22.23.4 or later** and npm (Astro 7 toolchain).

~~~sh
npm install
npm run dev
npm run build
~~~

The output of the static build is written to dist/.

## Repository layout

- src/content/docs/ — English content
- src/content/docs/ru/ — Russian content
- src/assets/sedrava-mark.svg — vector interpretation of the approved mark concept
- src/styles/brand.css — amethyst and matte gold visual theme
- public/branding/ — public assets
- .github/workflows/build.yml — CI build
- .github/workflows/deploy.yml — manual VDS deployment

## Release status

[**Sedrava 0.10.0**](https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0) was published on GitHub and [PyPI](https://pypi.org/project/sedrava/0.10.0/) on 31 October 2026. It includes text, records, bounded collections and multi-screen navigation. The release is experimental and not a production-support or 1.0 compatibility guarantee. The physical-device acceptance of the final 0.10 Android APK has not been documented. Historical 0.9/RC reports remain available as historical evidence.

The experimental 0.11 `sedrava build site` language feature is being developed in [draft PR #22](https://github.com/VasiliiBabkin/sedrava/pull/22); this documentation website itself uses **Astro/Starlight**, not the released 0.10 language generator.

## Deployment

The public site is statically served by Nginx with FASTPANEL on a VDS. Deployment runs automatically on pushes to main and can also be started manually via the [GitHub Actions workflow](https://github.com/VasiliiBabkin/sedrava-site/actions/workflows/deploy.yml), using SSH and tar.

For details, see DEPLOYMENT.md. Never commit SSH keys or any other server credentials.

## Visual identity

Amethyst #583C82, deep amethyst #35234F, matte gold #D5AD60 and ivory #F5F0E8. The SVG mark is a vector approximation of the approved Dynamic Cut brand concept and should receive a final visual comparison before production.
