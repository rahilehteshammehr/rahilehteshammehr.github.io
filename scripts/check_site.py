#!/usr/bin/env python3
"""Crawl built output: pages, assets, fragments, data, and deployment paths."""
from prepare_cv import settings
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument('directory', nargs='?', default='_site')
parser.add_argument('--baseurl', default='')
args = parser.parse_args()
root = Path(args.directory).resolve()
base = args.baseurl.rstrip('/')
cv_settings, manual_cv, cv_output = settings(Path(__file__).resolve().parents[1])
public_cv = root / cv_settings['published_file'].lstrip('/')
profile = json.loads((Path(__file__).resolve().parents[1] / '_data/profile.json').read_text())
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids = set(); self.refs = []; self.h1 = 0; self.main = 0; self.title = 0; self.lang = None; self.description = False
    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id {attrs["id"]}'
            self.ids.add(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'main': self.main += 1
        if tag == 'title': self.title += 1
        if tag == 'html': self.lang = attrs.get('lang')
        if tag == 'meta' and attrs.get('name') == 'description': self.description = bool(attrs.get('content'))
        for key in ('href', 'src'):
            if attrs.get(key): self.refs.append(attrs[key])

pages = {}
for path in root.rglob('*.html'):
    text = path.read_text()
    d = Document(); d.feed(text); pages[path] = d
    assert d.h1 == d.main == d.title == 1, (path, 'Missing/duplicate primary structure')
    assert d.lang == 'en' and d.description, (path, 'Missing language/description')
    for forbidden in ['Your Name', 'John Doe', 'none@example.org', 'Portrait to come', 'Compare prototypes', '{{', '{%']:
        assert forbidden not in text, (path, forbidden)
    assert profile['email'] in text, path
    assert base + cv_settings['published_file'] in d.refs, (path, 'Missing selected CV link')
for route in ('index.html', 'research/index.html', 'cv/index.html', 'beyond-physics/index.html', '404.html'):
    assert root / route in pages, f'Missing core page: {route}'
checked = 0
for path, d in pages.items():
    for reference in d.refs:
        url = urlsplit(reference)
        if url.scheme or url.netloc: continue
        route = unquote(url.path)
        if route.startswith('/'):
            assert not base or route.startswith(base+'/'), (path, f'Missing baseurl: {reference}')
            target = root / route[len(base):].lstrip('/')
        else:
            target = path.parent / route if route else path
        if target.is_dir(): target = target / 'index.html'
        target = target.resolve()
        assert target.is_relative_to(root), (path, reference)
        assert target.is_file(), (path, f'Broken local reference: {reference}')
        if url.fragment and target in pages:
            assert unquote(url.fragment) in pages[target].ids, (path, f'Broken fragment: {reference}')
        checked += 1
for private in ['main.tex','prototypes','research/template-research.md','scripts','docs','cv-source','review','PRODUCT.md','DESIGN.md','.cache','Gemfile']:
    assert not (root / private).exists(), f'Non-public file leaked: {private}'
assert public_cv.read_bytes().startswith(b'%PDF'), 'Invalid CV'
expected_cv = manual_cv if cv_settings['mode'] == 'manual' else cv_output
assert public_cv.read_bytes() == expected_cv.read_bytes(), 'Built PDF differs from the selected CV source; rebuild the site'
sitemap = ET.parse(root / 'sitemap.xml')
locations = [node.text for node in sitemap.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
sitemap_files = set()
for location in locations:
    route = unquote(urlsplit(location).path)
    assert not base or route.startswith(base + '/'), f'Missing sitemap baseurl: {location}'
    target = root / route[len(base):].lstrip('/')
    if target.is_dir(): target = target / 'index.html'
    target = target.resolve()
    assert target.is_relative_to(root) and target.is_file(), f'Broken sitemap URL: {location}'
    assert target not in sitemap_files, f'Duplicate sitemap URL: {location}'
    sitemap_files.add(target)
assert root / '404.html' not in sitemap_files, '404 must not appear in sitemap'
assert set(pages) - {root / '404.html'} <= sitemap_files, 'Public pages missing from sitemap'
assert public_cv in sitemap_files, 'CV missing from sitemap'
print(f'PASS: {len(pages)} HTML pages, {checked} local references and fragments, PDF, sitemap, and private-source exclusions (baseurl={base!r}).')
