import { readFileSync, existsSync } from 'node:fs';
import { resolve, join } from 'node:path';
const root=resolve('src/content/docs');
const slugs=['index','getting-started','platform','examples','language-overview','roadmap','releases','text-010','rust-native','sedravasql','benchmarks'];
let checked=0;
for(const prefix of ['', 'ru/']) for(const slug of slugs){
 const path=join(root,prefix,slug+(slug==='index'?'.mdx':'.md'));
 const text=readFileSync(path,'utf8');
 if(!text.startsWith('---\n'))throw Error('Missing frontmatter: '+path);
 if(/pypi\.org|pip install|stable 0\.11|стабильн[^\n]*0\.11/i.test(text))throw Error('Legacy distribution in active docs: '+path);
 if(['index','getting-started','releases','rust-native','roadmap'].includes(slug)&&!text.includes('0.12.0-alpha.2'))throw Error('Missing current version: '+path);
 for(const m of text.matchAll(/(?:\]\(|href="|link: )\/(ru\/)?([a-z0-9-]+)\//g)){
  const route=(m[1]||'')+m[2];
  if(!existsSync(join(root,route+'.md'))&&!existsSync(join(root,route+'.mdx')))throw Error('Broken local route: '+route);
 }
 checked++;
}
console.log('PASS: '+checked+' Rust-first EN/RU pages; no historical distribution instructions');
