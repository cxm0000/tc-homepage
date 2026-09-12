"""Run from the project root: python3 scripts/check-seo.py."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.metas, self.images = [], [], {}, []
        self.schema, self.in_schema, self.headings = '', False, 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'a': self.links.append(attrs.get('href', ''))
        if tag == 'meta': self.metas[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'img': self.images.append(attrs['src'])
        if tag == 'h1': self.headings += 1
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.in_schema = True
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
    def handle_data(self, data):
        if self.in_schema: self.schema += data
    def handle_endtag(self, tag):
        if tag == 'script': self.in_schema = False

page = Page()
page.feed(Path('index.html').read_text())
assert page.headings == 1
assert len(page.ids) == len(set(page.ids))
assert page.canonical == page.metas['og:url'] == 'https://tangcai.se/'
assert 'noindex' not in page.metas['robots']
for path in page.images: assert Path(path).is_file(), path
for link in page.links:
    if link.startswith('#') and link != '#': assert link[1:] in page.ids, link
nodes = json.loads(page.schema)['@graph']
node_ids = {node['@id'] for node in nodes}
def check_refs(value):
    if isinstance(value, dict):
        if set(value) == {'@id'}: assert value['@id'] in node_ids, value
        for child in value.values(): check_refs(child)
    elif isinstance(value, list):
        for child in value: check_refs(child)
check_refs(nodes)
apps = [node for node in nodes if node['@type'] == 'SoftwareApplication']
assert len(apps) == 5
for app in apps:
    assert app['url'] in page.links, app['name']
    assert app['@id'].split('#')[1] in page.ids
    assert app['name'] in Path('llms.txt').read_text()
    assert not any(key in app for key in ('aggregateRating', 'offers', 'review'))
robot = RobotFileParser()
robot.parse(Path('robots.txt').read_text().splitlines())
for agent in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'PerplexityBot'):
    assert robot.can_fetch(agent, page.canonical), agent
locs = ET.parse('sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
assert [loc.text for loc in locs] == [page.canonical]
print('Passed: metadata, canonical, five linked app entities, schema references, local images, section anchors, sitemap, and crawler access.')
