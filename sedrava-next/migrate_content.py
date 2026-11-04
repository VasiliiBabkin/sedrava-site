"""One-time reviewed content migration; produces Markdown source, never patches HTML output."""
from html.parser import HTMLParser
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
class ReviewedHome(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.links=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag not in ('div','article','p','h2','h3','span','a','strong','code','img'):raise ValueError('Unreviewed MDX element '+tag)
        if tag in ('div','article','p','span'):self.parts.append('\n\n')
        elif tag in ('h2','h3'):self.parts.append('\n\n'+'#'*int(tag[1])+' ')
        elif tag=='a':self.parts.append('[');self.links.append(attrs['href'])
        elif tag=='strong':self.parts.append('**')
        elif tag=='code':self.parts.append('`')
    def handle_endtag(self,tag):
        if tag=='a':self.parts.append(']('+self.links.pop()+')')
        elif tag=='strong':self.parts.append('**')
        elif tag=='code':self.parts.append('`')
        else:self.parts.append('\n\n')
    def handle_data(self,data):self.parts.append(data)
def migrate(check=False):
    records=[]
    for source in sorted((ROOT/'src/content/docs').rglob('*')):
        if source.suffix not in ('.md','.mdx'):continue
        relative=source.relative_to(ROOT/'src/content/docs');locale='ru' if relative.parts[0]=='ru' else 'en'
        target=ROOT/'sedrava-next/content'/locale/('home.md' if source.stem=='index' else source.name)
        raw=source.read_text();body=re.sub(r'\A---\n.*?\n---\n','',raw,count=1,flags=re.S)
        if source.suffix=='.mdx':
            # Preserve fenced code verbatim; convert only the reviewed static HTML around it.
            chunks=re.split(r'((?:~~~|```)[^\n]*\n.*?(?:~~~|```))',body,flags=re.S);out=[]
            for i,chunk in enumerate(chunks):
                if i%2:out.append(chunk)
                else:
                    parser=ReviewedHome();parser.feed(chunk);converted=re.sub(r'\n[ \t]+','\n',''.join(parser.parts));converted=re.sub(r'\n{3,}','\n\n',converted);out.append(converted)
            body='\n'.join(out).strip()+'\n'
        else:body=raw
        # Correct the obsolete implementation claim only in the migrated copy. Production content stays unchanged.
        body=body.replace('This official documentation site uses Astro/Starlight separately.','This documentation website is generated from Sedrava sources with the experimental compiler in PR #37, based on PR #36. Website generation is not part of the published 0.10.0 package.')
        body=body.replace('Сайт документации отдельно собирается через Astro/Starlight.','Этот сайт документации создаётся из исходников Sedrava с экспериментальным компилятором PR #37 на базе PR #36. В опубликованную версию 0.10.0 генерация сайтов не входит.')
        body=body.replace('which is independently built with Astro/Starlight in','which is generated directly by the experimental Sedrava compiler from the sources in')
        body=body.replace('Этот официальный сайт документации создаётся отдельно через Astro/Starlight в','Этот сайт документации создан на Sedrava из исходников в')
        # Migrated website release claims follow the actual native Sedrava integration.
        body=body.replace('**Draft PR #22**, not included in 0.10.0','**Experimental PRs #36 and #37**, not included in 0.10.0')
        body=body.replace('**Черновой PR №22**, отсутствует в 0.10.0','**Экспериментальные PR №36 и №37**, отсутствует в 0.10.0')
        fenced=lambda value:re.findall(r'(?:~~~|```)[^\n]*\n(.*?)(?:~~~|```)',value,re.S)
        assert fenced(raw)==fenced(body),'Code indentation/content lost during migration: '+str(source)
        if check:
            assert target.read_text()==body,'Migrated content differs from the reviewed transformation: '+str(target)
        else:target.write_text(body)
        records.append({'source':source.relative_to(ROOT).as_posix(),'target':target.relative_to(ROOT).as_posix(),'route':('/ru/' if locale=='ru' else '/')+('' if source.stem=='index' else source.stem+'/'),'reviewed_mdx':source.suffix=='.mdx','source_sha256':hashlib.sha256(raw.encode()).hexdigest(),'migrated_sha256':hashlib.sha256(body.encode()).hexdigest()})
    manifest=json.dumps(records,ensure_ascii=False,indent=2)+'\n'
    if check:assert (ROOT/'sedrava-next/migration.json').read_text()==manifest,'Migration receipt differs'
    else:(ROOT/'sedrava-next/migration.json').write_text(manifest)
    print('PASS: '+str(len(records))+' original EN/RU pages mapped without content loss')
if __name__=='__main__':migrate('--check' in sys.argv)
