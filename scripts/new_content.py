#!/usr/bin/env python3
"""Create an editable draft without overwriting existing content. No dependencies."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('kind', choices=['post', 'project', 'page'])
parser.add_argument('title', help='Put a multi-word title in quotes.')
parser.add_argument('--slug', help='Optional stable URL slug, using lowercase letters, numbers and hyphens.')
parser.add_argument('--date', type=date.fromisoformat, default=date.today(), help='Post date as YYYY-MM-DD.')
parser.add_argument('--photos', action='store_true', help='Use a photo template (posts and projects).')
args = parser.parse_args()
if not args.title.strip():
    parser.error('The title cannot be blank.')
if args.photos and args.kind not in ('post', 'project'):
    parser.error('--photos is only available for posts and projects.')
slug = args.slug or re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', args.title).encode('ascii', 'ignore').decode().lower()).strip('-')
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug):
    parser.error('Provide --slug with lowercase letters, numbers and hyphens.')
folder = ROOT / {'post': '_posts', 'project': '_projects', 'page': '_pages'}[args.kind]
filename = f'{args.date.isoformat()}-{slug}.md' if args.kind == 'post' else f'{slug}.md'
target = folder / filename
if args.kind == 'post' and any(folder.glob(f'????-??-??-{slug}.md')):
    parser.error(f'A post already uses the URL /beyond-physics/{slug}/. Choose another --slug.')
template = f'photo-{args.kind}' if args.photos else args.kind
content = (ROOT / 'docs/templates' / f'{template}.md').read_text()
content = re.sub(r'^title: .*$', lambda _: 'title: ' + json.dumps(args.title, ensure_ascii=False), content, count=1, flags=re.M)
if 'published: false' not in content.split('---')[1]:
    content = content.replace('---\n', '---\npublished: false\n', 1)
if args.kind == 'page':
    content = content.replace('permalink: /your-page/', f'permalink: /{slug}/')
try:
    with target.open('x') as out:
        out.write(content)
except FileExistsError:
    parser.error(f'{target.relative_to(ROOT)} already exists; it was not overwritten.')
print(f'Created draft: {target.relative_to(ROOT)}')
print('Edit the file, preview with npm run dev:drafts, then remove published: false when ready.')
if args.photos:
    print('Replace the example image paths, alt text and captions with your own photographs.')
if args.kind == 'page':
    print('Link to the page from existing content or add it to _data/navigation.yml.')
