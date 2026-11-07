import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://sedrava.virtreal.ru',
  integrations: [
    starlight({
      disable404Route: true,
      title: 'Sedrava',
      description: 'Official website and documentation of the experimental Sedrava programming language.',
      logo: {
        src: './public/brand/sedrava-logo-primary.png',
        alt: 'Sedrava',
      },
      favicon: '/brand/favicon.ico',
      head: [
        { tag: 'link', attrs: { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/brand/sedrava-logo-32.png' } },
        { tag: 'link', attrs: { rel: 'apple-touch-icon', sizes: '180x180', href: '/brand/sedrava-logo-180.png' } },
        { tag: 'link', attrs: { rel: 'manifest', href: '/brand/site.webmanifest' } },
        { tag: 'meta', attrs: { property: 'og:image', content: 'https://sedrava.virtreal.ru/brand/sedrava-og.png' } },
        { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
        { tag: 'meta', attrs: { name: 'twitter:image', content: 'https://sedrava.virtreal.ru/brand/sedrava-og.png' } },
      ],
      customCss: ['./src/styles/brand.css'],
      locales: {
        root: { label: 'English', lang: 'en' },
        ru: { label: 'Русский', lang: 'ru' },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/VasiliiBabkin/sedrava' },
      ],
      editLink: {
        baseUrl: 'https://github.com/VasiliiBabkin/sedrava-site/edit/main/',
      },
      sidebar: [
        {
          label: 'Start',
          translations: { ru: 'Начало' },
          items: [
            { slug: 'getting-started' },
            { slug: 'examples' },
          ],
        },
        {
          label: 'Learn',
          translations: { ru: 'Изучение' },
          items: [
            { slug: 'language-overview' },
            { slug: 'text-010' },
          ],
        },
        {
          label: 'Project',
          translations: { ru: 'Проект' },
          items: [
            { slug: 'roadmap' },
            { slug: 'releases' },
          ],
        },
      ],
    }),
  ],
});
