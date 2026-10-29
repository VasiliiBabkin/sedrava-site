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

Sedrava 0.9.0a1 is the published experimental alpha baseline. First-class text is implemented in source as unreleased 0.10.0.dev0; the full 0.10 release is not published. Neither version is production-ready. The website documents both statuses separately.

## Deployment

The public site is statically served by Nginx with FASTPANEL on a VDS. Deployment is manual via the [GitHub Actions workflow](https://github.com/VasiliiBabkin/sedrava-site/actions/workflows/deploy.yml), using SSH and tar.

For details, see DEPLOYMENT.md. Never commit SSH keys or any other server credentials.

## Visual identity

Amethyst #583C82, deep amethyst #35234F, matte gold #D5AD60 and ivory #F5F0E8. The SVG mark is a vector approximation of the approved Dynamic Cut brand concept and should receive a final visual comparison before production.
