import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

export default defineConfig({
  site: 'https://sedrava.virtreal.ru',
  integrations: [
    starlight({
      title: 'Sedrava',
      // English pages live directly in src/content/docs and use the site root.
      // Russian pages live in src/content/docs/ru and use the /ru/ prefix.
      locales: {
        root: { label: 'English', lang: 'en' },
        ru: { label: 'Русский', lang: 'ru' },
      },
      social: [
        { icon: 'github', label: 'GitHub', href: 'https://github.com/VasiliiBabkin/intent-lang' },
      ],
      sidebar: [
        {
          label: 'Guides',
          translations: { ru: 'Руководства' },
          items: [
            { label: 'Getting started', translations: { ru: 'Начало работы' }, slug: 'getting-started' },
          ],
        },
      ],
    }),
  ],
});
