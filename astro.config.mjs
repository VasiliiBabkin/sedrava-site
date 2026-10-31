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
        src: './src/assets/sedrava-mark.svg',
        alt: 'Sedrava',
      },
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
          ],
        },
      ],
    }),
  ],
});
