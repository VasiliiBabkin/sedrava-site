// Verify bilingual docs and the published 0.10.0 release status before build/deploy.
import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';

const root = resolve('src/content/docs');
const slugs = ['index', 'getting-started', 'examples', 'language-overview', 'roadmap', 'text-010'];
const published = 'https://pypi.org/project/sedrava/0.10.0/';
const release = 'https://github.com/VasiliiBabkin/sedrava/releases/tag/v0.10.0';
const stale = [
  /0\.10\.0\.dev0/i,
  /0\.10\.0rc2\s*[·—-]\s*(?:published|опубликован)/i,
  /sedrava is not published on pypi/i,
  /пакета sedrava на pypi пока нет/i,
  /0\.10\s*(?:is|remains)\s*unreleased/i,
  /0\.10\s*(?:не выпущена|ещё не выпущена)/i,
  /unreleased 0\.10/i,
];

let checked = 0;
for (const prefix of ['', 'ru/']) {
  for (const slug of slugs) {
    const path = join(root, prefix, slug + (slug === 'index' ? '.mdx' : '.md'));
    if (!existsSync(path)) throw new Error('Missing bilingual page: ' + path);
    const text = readFileSync(path, 'utf8');
    if (!text.startsWith('---\n')) throw new Error('Missing frontmatter: ' + path);
    for (const required of ['0.10.0', published, release]) {
      if (!text.includes(required)) throw new Error('Missing release fact (' + required + '): ' + path);
    }
    for (const p of stale) {
      if (p.test(text)) throw new Error('Stale unreleased status: ' + path + ' / ' + p);
    }
    const routes = new Set([...text.matchAll(/(?:\]\(|href="|link: )\/(ru\/)?([a-z0-9-]+)\//g)].map(m => (m[1] ? 'ru/' : '') + m[2]));
    for (const route of routes) {
      if (route.startsWith('branding')) continue;
      const candidate = join(root, route + '.md');
      const home = join(root, route + '.mdx');
      if (!existsSync(candidate) && !existsSync(home)) throw new Error('Broken local route: /' + route + '/ in ' + path);
    }
    checked++;
  }
}
console.log('PASS: ' + checked + ' EN/RU pages have current 0.10.0 status and local routes');
