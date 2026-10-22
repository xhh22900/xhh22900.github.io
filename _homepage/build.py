"""Rebuild the static homepage: python _homepage/build.py (Python standard library)."""
from pathlib import Path
import html
import json
import re
from string import Template

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / '_data' / 'academic.json').read_text(encoding='utf-8'))
CITATIONS = json.loads((ROOT / '_data' / 'citations.json').read_text(encoding='utf-8'))


def esc(text):
    return html.escape(str(text), quote=True)


def bi(value, en=None, tag='span', css=''):
    if en is None:
        zh, en = value['zh'], value['en']
    else:
        zh = value
    extra = f' class="{css}"' if css else ''
    return f'<{tag}{extra}><span data-lang="zh" lang="zh-CN">{esc(zh)}</span> <span data-lang="en" lang="en">{esc(en)}</span></{tag}>'


def rich(text):
    value = esc(text)
    value = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', value)
    value = re.sub(r'\*(.+?)\*', r'<em>\1</em>', value)
    return re.sub(r'\^\{(.+?)\}', r'<sup>\1</sup>', value)


def research():
    blocks = []
    for item in DATA['research']:
        blocks.append(f'''<article class="research-item">
          {bi(item['title'], tag='h3')}
          <div class="research-detail">{bi(item['text'], tag='p')}
          <div class="research-bottom">{bi(item['note'], css='research-note')}<button class="research-link" type="button" data-field="{item['field']}" aria-label="View related publications">{bi('相关论文', 'Related papers')} →</button></div></div>
        </article>''')
    return '\n'.join(blocks)


def papers():
    blocks = []
    # The chronological overview is independent of first-author / collaboration filters.
    for item in sorted(DATA['publications'], key=lambda p: (-p['year'], not p['first_author'], p['id'])):
        tags = []
        if item['letter']:
            tags.append('<span class="paper-tag letter">PRC Letter</span>')
        if item['first_author']:
            tags.append(bi('第一作者', 'First author', css='paper-tag first-author'))
        highlight = bi(item['highlight'], tag='p', css='paper-highlight') if item.get('highlight') else ''
        citation = CITATIONS[str(item['id'])]
        arxiv = f'<a href="{esc(citation["arxiv_url"])}" target="_blank" rel="noopener noreferrer">arXiv ↗</a>' if citation.get('arxiv_url') else ''
        bib_id = f'bibtex-{item["id"]}'
        actions = f'''<div class="paper-actions">
            <a href="{esc(item['url'])}" target="_blank" rel="noopener noreferrer">DOI ↗</a>{arxiv}
            <details class="citation-details"><summary>BibTeX</summary><div class="citation-panel">
              <div class="citation-toolbar"><button type="button" data-copy-bib="{bib_id}">{bi('复制 BibTeX', 'Copy BibTeX')}</button><a href="{esc(citation['file'])}" download>{bi('下载 .bib', 'Download .bib')}</a><span class="copy-feedback" role="status" aria-live="polite"></span></div>
              <pre id="{bib_id}" tabindex="0">{esc(citation['bibtex'])}</pre>
            </div></details>
          </div>'''
        search = re.sub(r'<[^>]+>', '', ' '.join([item['title'], item['authors'], item['journal'], str(item['year']), item.get('search_keywords', '')]))
        blocks.append(f'''<article class="paper" data-id="{item['id']}" data-selected="{str(item['selected']).lower()}" data-first="{str(item['first_author']).lower()}" data-field="{item['field']}" data-search="{esc(search.lower())}">
          <div class="paper-year">{item['year']}<span class="paper-index">[{item['id']}]</span></div>
          <div class="paper-content"><div class="paper-tags">{''.join(tags)}</div>
          <h3><a href="{esc(item['url'])}" target="_blank" rel="noopener noreferrer">{rich(item['title'])}<span class="external-arrow" aria-hidden="true">↗</span></a></h3>
          <p class="paper-authors">{rich(item['authors'])}</p>
          <p class="paper-journal">{rich(item['journal'])}</p>{highlight}{actions}</div>
        </article>''')
    return '\n'.join(blocks)


def manuscripts():
    blocks = []
    for item in DATA['manuscripts']:
        title = rich(item['title'])
        if item['url']:
            title = f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{title} ↗</a>'
        summary = bi(item['summary'], tag='p', css='manuscript-summary') if item.get('summary') else ''
        blocks.append(f'''<article class="manuscript">{bi(item['status'], css='eyebrow manuscript-status')}<h4>{title}</h4><p class="paper-authors">{rich(item['authors'])}</p>{summary}</article>''')
    return '\n'.join(blocks)


def experience():
    blocks = []
    for item in DATA['experience']:
        date = bi(item.get('date_zh', item['date']), item['date'], css='timeline-date')
        detail = bi(item['detail'], tag='p', css='timeline-detail') if item['detail']['zh'] else ''
        blocks.append(f'''<article class="timeline-item">{date}<div>{bi(item['title'], tag='h3')}{bi(item['place'], tag='p', css='timeline-place')}{detail}</div></article>''')
    return '\n'.join(blocks)


def talks():
    return '\n'.join(f'''<article class="talk"><span class="talk-date">{item['date']}</span><div>{bi(item['title'], item.get('title_en', item['title']), tag='h4')}{bi(item['event'], tag='p')}</div></article>''' for item in DATA['talks'])


def main():
    grant = DATA['grant']
    replacements = {
        'research': research(), 'publications': papers(), 'manuscripts': manuscripts(),
        'experience': experience(), 'talks': talks(),
        'grant_name': bi(grant['name'], tag='h3'), 'grant_project': bi(grant['project'], tag='p'),
        'grant_role': bi(grant['role']), 'grant_id': esc(grant['id']),
        'published_count': str(len(DATA['publications'])),
        'first_count': str(sum(p['first_author'] for p in DATA['publications'])),
        'updated': DATA['updated'],
    }
    template = (ROOT / '_homepage' / 'index.template.html').read_text(encoding='utf-8')
    output = Template(template).substitute(replacements)
    output = re.sub(r'<span data-lang="zh"(?! lang=)', '<span data-lang="zh" lang="zh-CN"', output)
    output = re.sub(r'<span data-lang="en"(?! lang=)', '<span data-lang="en" lang="en"', output)
    output = output.replace('</span><span data-lang=', '</span> <span data-lang=')
    (ROOT / 'index.html').write_text(output, encoding='utf-8')
    print('Built index.html with', replacements['published_count'], 'journal articles.')


if __name__ == '__main__':
    main()
