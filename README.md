# Sedrava website

Official website and documentation for the Sedrava programming language.

Website: https://sedrava.virtreal.ru

## Development

Requires Node.js 20.19+ or 22.12+.

```sh
npm install
npm run dev
npm run build
```

Built with Astro and Starlight. English is the default documentation language; Russian is also supported.

## Deployment

The site is statically generated into `dist/`. Deployment to the VDS will be configured separately using restricted SSH credentials stored in GitHub Actions secrets. Never commit server credentials.
