#!/usr/bin/env python3
"""Generate the automatic CV source. prepare_cv.py selects the published PDF."""
import json
import yaml
from itertools import zip_longest
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
profile = json.loads((ROOT / '_data/profile.json').read_text())
cv = json.loads((ROOT / '_data/cv.json').read_text())
projects = []
for path in (ROOT / '_projects').glob('*.md'):
    front = path.read_text().split('---', 2)[1]
    project = yaml.safe_load(front)
    if project.get('published', True) is not False:
        projects.append(project)
projects.sort(key=lambda item: item['order'])
output = ROOT / '.cache/generated-cv.pdf'
output.parent.mkdir(exist_ok=True)
ink, muted, accent, line = map(colors.HexColor, ['#303b40', '#5b666c', '#176778', '#dce3e6'])
styles = {
    'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=ink, spaceAfter=7),
    'contact': ParagraphStyle('contact', fontName='Helvetica', fontSize=9.5, leading=14, textColor=accent, spaceAfter=12),
    'h2': ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=accent, spaceBefore=10, spaceAfter=6, keepWithNext=True),
    'h3': ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=10, leading=12.5, textColor=ink, spaceAfter=2, keepWithNext=True),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=12.5, textColor=ink, spaceAfter=3),
    'meta': ParagraphStyle('meta', fontName='Helvetica', fontSize=9, leading=11.5, textColor=muted, spaceAfter=2),
}
def clean(text):
    return escape(text.replace('–', '-').replace('—', '-').replace('’', "'").replace('“', '"').replace('”', '"'))
def p(text, style='body'):
    return Paragraph(clean(text), styles[style])
def heading(title):
    story.append(p(title, 'h2'))
def entry(title, meta, detail, extra=None):
    elements = [p(title, 'h3'), p(meta, 'meta'), p(detail)]
    if extra: elements.append(p(extra, 'meta'))
    elements.append(Spacer(1, 2))
    story.append(KeepTogether(elements))

def footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(line)
    canvas.line(44, 37, width-44, 37)
    canvas.setFillColor(muted)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(44, 24, f"{profile['name']} | Updated {cv['updated']}")
    canvas.drawRightString(width-44, 24, str(doc.page))
    canvas.restoreState()

contact = f'<a href="mailto:{escape(profile["email"])}" color="#176778">{clean(profile["email"])}</a>  |  {clean(profile["location"])}'
if profile.get('linkedin'):
    contact += f'  |  <a href="{escape(profile["linkedin"])}" color="#176778">LinkedIn</a>'
story = [p(profile['name'], 'name'), Paragraph(contact, styles['contact'])]
heading('Education')
e = cv['education']
entry(e['degree'], f"{e['institution']}, {e['location']} | {e['period']}", f"GPA: {e['gpa']} ({e['standing'].lower()}).")
heading('Research interests')
story.append(p('; '.join(profile['interests'])+'.'))
heading('Research experience')
for r in projects:
    if r['category'] != 'Undergraduate research': continue
    entry(r['title'], r['period'], r['summary'], f"Supervisor: {r['supervisor']}" if r.get('supervisor') else None)
heading('Academic projects')
for item in projects:
    if item['category'] != 'Academic project': continue
    entry(item['title'], item['period'], item['summary'], f"Supervisor: {item['supervisor']}" if item.get('supervisor') else None)
story.append(PageBreak())
heading('Honors & awards')
for item in cv['honors']:
    entry(item['title'], item['period'], item['detail'])
heading('Teaching')
for item in cv['teaching']:
    meta = item['organization'] + (f" | {item['period']}" if item.get('period') else '')
    entry(item['title'], meta, item['detail'])
heading('Skills & languages')
for item in cv['skills'] + cv['languages']:
    story.append(Paragraph(f"<b>{clean(item['label'])}:</b> {clean(item['value'])}", styles['body']))
heading('Selected coursework')
rows = [[p('Course', 'h3'), p('Grade / 20', 'h3'), p('Course', 'h3'), p('Grade / 20', 'h3')]]
midpoint = (len(cv['courses']) + 1) // 2
for left, right in zip_longest(cv['courses'][:midpoint], cv['courses'][midpoint:]):
    rows.append([p(left['name']), p(str(left['grade']).split('/')[0]),
                 p(right['name']) if right else '', p(str(right['grade']).split('/')[0]) if right else ''])
table = Table(rows, colWidths=[170,65,170,65], hAlign='LEFT', repeatRows=1)
table.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),3),('LINEBELOW',(0,0),(-1,0),.6,line)]))
story.append(table)
heading('Service')
for item in cv['service']:
    entry(item['title'], f"{item['organization']} | {item['period']}", item['detail'])

doc = SimpleDocTemplate(str(output), pagesize=A4, rightMargin=44, leftMargin=44, topMargin=38, bottomMargin=50, title=f"{profile['name']} - Curriculum vitae", author=profile['name'])
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(output)
