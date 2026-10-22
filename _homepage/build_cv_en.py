"""Build the public English CV from the shared academic records and cv_en.json.

Requires reportlab. Output: assets/files/huihui-xie-academic-cv-en.pdf.
"""
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr
import json
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / '_data/academic.json').read_text(encoding='utf-8'))
CV = json.loads((ROOT / '_data/cv_en.json').read_text(encoding='utf-8'))
OUTPUT = ROOT / 'assets/files/huihui-xie-academic-cv-en.pdf'
PAGE_W, PAGE_H = A4
LEFT = RIGHT = 45
TOP, BOTTOM = 39, 39
WIDTH = PAGE_W - LEFT - RIGHT - 12
INK = colors.HexColor('#202832')
MUTED = colors.HexColor('#566170')
BLUE = colors.HexColor('#244967')


def fonts():
    directory = Path(os.environ.get('WINDIR', 'C:/Windows')) / 'Fonts'
    files = {'Serif': 'times.ttf', 'SerifBold': 'timesbd.ttf', 'SerifItalic': 'timesi.ttf',
             'SerifBoldItalic': 'timesbi.ttf', 'Sans': 'arial.ttf', 'SansBold': 'arialbd.ttf'}
    if all((directory / filename).exists() for filename in files.values()):
        for name, filename in files.items():
            pdfmetrics.registerFont(TTFont(name, str(directory / filename)))
        pdfmetrics.registerFontFamily('Serif', normal='Serif', bold='SerifBold', italic='SerifItalic', boldItalic='SerifBoldItalic')
        pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='SansBold', italic='Sans', boldItalic='SansBold')
        return 'Serif', 'Sans', 'SansBold'
    return 'Times-Roman', 'Helvetica', 'Helvetica-Bold'


SERIF, SANS, SANS_BOLD = fonts()
BODY = ParagraphStyle('Body', fontName=SERIF, fontSize=10.2, leading=14,
                      textColor=INK, alignment=TA_LEFT, spaceAfter=4,
                      allowWidows=False, allowOrphans=False)
STYLES = {
    'body': BODY,
    'name': ParagraphStyle('Name', parent=BODY, fontName=SANS_BOLD, fontSize=24, leading=29, spaceAfter=4),
    'role': ParagraphStyle('Role', parent=BODY, fontName=SANS, fontSize=10.5, leading=15, spaceAfter=4),
    'contact': ParagraphStyle('Contact', parent=BODY, fontName=SANS, fontSize=9, leading=13, spaceAfter=2),
    'heading': ParagraphStyle('Heading', parent=BODY, fontName=SANS_BOLD, fontSize=11.5, leading=16, spaceBefore=9, spaceAfter=5, keepWithNext=True),
    'subheading': ParagraphStyle('Subheading', parent=BODY, fontName=SANS_BOLD, fontSize=10.1, leading=14, spaceBefore=6, spaceAfter=5, keepWithNext=True),
    'small': ParagraphStyle('Small', parent=BODY, fontName=SANS, fontSize=9, leading=12.5, textColor=MUTED),
    'detail': ParagraphStyle('Detail', parent=BODY, fontSize=10.1, leading=13.8, spaceAfter=6),
    'publication': ParagraphStyle('Publication', parent=BODY, fontSize=10.2, leading=13.7, leftIndent=25, firstLineIndent=-25, spaceAfter=7),
    'date': ParagraphStyle('Date', parent=BODY, fontName=SANS, fontSize=9.1, leading=13, textColor=MUTED, spaceAfter=0),
    'cell': ParagraphStyle('Cell', parent=BODY, fontSize=10.1, leading=13.6, spaceAfter=1),
}


def ascii_punctuation(text):
    return text.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"').replace('—', '-').replace('–', '-').replace('‐', '-')


def rich(text):
    text = escape(ascii_punctuation(text))
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    return re.sub(r'\^\{(.+?)\}', r'<super>\1</super>', text)


def paragraph(text, style='body', raw=False):
    return Paragraph(ascii_punctuation(text) if raw else rich(text), STYLES[style])


def link(label, url):
    return f'<link href={quoteattr(url)} color="#244967">{escape(label)}</link>'


def heading(text):
    return paragraph(text, 'heading')


def timeline(entries, date_width=102):
    rows = [[paragraph(date, 'date'), [paragraph(line, 'cell', raw=True) for line in lines]] for date, lines in entries]
    table = Table(rows, colWidths=[date_width, WIDTH - date_width], hAlign='LEFT')
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, -1), 10), ('RIGHTPADDING', (1, 0), (1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    return table


def page_one():
    story = [paragraph('Hui Hui Xie', 'name'),
             paragraph('Dingxin Postdoctoral Researcher | College of Physics, Jilin University', 'role')]
    story += [paragraph(link(DATA['email'], 'mailto:' + DATA['email']) + ' | Changchun, China', 'contact', raw=True),
              paragraph(link('xhh22900.github.io', 'https://xhh22900.github.io/') + ' | ORCID: ' + link(DATA['orcid'], 'https://orcid.org/' + DATA['orcid']), 'contact', raw=True)]
    story.append(heading('Research overview'))
    story.append(paragraph('<b>14 published journal articles, including seven as first author.</b> First-author publications include a <i>Physical Review C</i> Letter. One first-author manuscript is under review at <i>Physical Review Letters</i>.', raw=True))
    story.append(heading('Research interests'))
    for interest in CV['research_interests']:
        story.append(paragraph(interest))
    story.append(heading('Appointments and education'))
    story.append(timeline([
        ('Dec 2024 - present', ['<b>Dingxin Postdoctoral Researcher</b>, Jilin University', 'Advisor: Jian Li']),
        ('Sep 2021 - Sep 2024', ['<b>Ph.D. in Particle and Nuclear Physics</b>, Jilin University', 'Advisor: Jian Li', 'Thesis: ' + escape(CV['thesis'])]),
        ('Sep 2018 - Jun 2021', ["<b>Master's degree in Theoretical Physics</b>, Jilin University", 'Advisors: Li Guang Jiao and Guo-Mo Zeng', 'Quantum information with Guo-Mo Zeng (about two years); precision atomic calculations with Li Guang Jiao (about one year).']),
        ('Sep 2014 - Jun 2018', ["<b>Bachelor's degree in Electronic Science and Technology</b>", 'Changchun University of Science and Technology']),
    ]))
    story.append(heading('Research funding'))
    story.append(paragraph('<b>China Postdoctoral Science Foundation, General Program (78th batch)</b><br/>Principal investigator | Grant 2025M783390 | December 2025<br/>Microscopic study of finite-nuclear-size effects in hydrogenlike ions.', raw=True))
    story.append(heading('Selected research contributions'))
    for item in CV['contributions']:
        story.append(KeepTogether([paragraph(item, 'detail', raw=True)]))
    return story


def reference(paper):
    text = f"[{paper['id']}] " + rich(paper['authors']) + ', "' + rich(paper['title']) + '," '
    text += f'<link href={quoteattr(paper["url"])} color="#244967">{rich(paper["journal"])}</link>'
    if paper['letter']:
        text += ' (Letter)'
    return paragraph(text + '.', 'publication', raw=True)


def page_two():
    story = [heading('Published journal articles'), paragraph('14 articles, seven as first author. The applicant\'s name is shown in bold.', 'small'), paragraph('First-author articles', 'subheading')]
    story += [KeepTogether([reference(p)]) for p in DATA['publications'] if p['first_author']]
    story.append(paragraph('Coauthored articles', 'subheading'))
    story += [KeepTogether([reference(p)]) for p in DATA['publications'] if not p['first_author']]
    return story


def page_three():
    story = [heading('Manuscripts and preprints')]
    for i, manuscript in enumerate(DATA['manuscripts'], 1):
        text = f'[S{i}] ' + rich(manuscript['authors']) + ', "' + rich(manuscript['title']) + '." '
        if i == 1:
            text += 'Submitted to <i>Physical Review Letters</i> (under review).'
        else:
            text += link('arXiv:2605.25390 (2026)', manuscript['url']) + '.'
        story.append(KeepTogether([paragraph(text, 'publication', raw=True)]))
    story.append(heading('Selected oral presentations'))
    dates = ['Jun 2026', 'Mar 2024', 'Apr 2023', 'Aug 2022']
    story.append(timeline([(date, [escape(talk['title_en']), escape(talk['event']['en'].replace(' · ', ', '))]) for date, talk in zip(dates, DATA['talks'])], date_width=66))
    story.append(heading('Collaboration and graduate research support'))
    story.append(paragraph(CV['collaboration'], 'detail'))
    story.append(heading('Numerical methods and technical skills'))
    for skill in CV['skills']:
        story.append(KeepTogether([paragraph(skill, 'detail', raw=True)]))
    return story


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.states = []

    def showPage(self):
        self.states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        count = len(self.states)
        for state in self.states:
            self.__dict__.update(state)
            self.saveState()
            self.setFont(SANS, 8)
            self.setFillColor(MUTED)
            if self._pageNumber > 1:
                self.drawString(LEFT, PAGE_H - 24, 'Hui Hui Xie | Curriculum vitae')
            self.drawString(LEFT, 20, 'Updated 22 October 2026')
            self.drawRightString(PAGE_W - RIGHT, 20, f'{self._pageNumber} / {count}')
            self.restoreState()
            super().showPage()
        super().save()


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, leftMargin=LEFT, rightMargin=RIGHT,
        topMargin=TOP, bottomMargin=BOTTOM, title='Hui Hui Xie Curriculum Vitae', author='Hui Hui Xie',
        subject='Nuclear structure and precision atomic physics', pageCompression=1)
    story = page_one() + [PageBreak()] + page_two() + [PageBreak()] + page_three()
    document.build(story, canvasmaker=NumberedCanvas)
    print(OUTPUT)


if __name__ == '__main__':
    main()
