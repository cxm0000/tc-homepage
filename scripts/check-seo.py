"""Run from the project root: python3 scripts/check-seo.py."""
import argparse
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

parser = argparse.ArgumentParser()
parser.add_argument('--site-url', default='https://tangcai.se/')
site_url = parser.parse_args().site_url.replace('http://', 'https://', 1).rstrip('/') + '/'

page = Page()
page.feed(Path('index.html').read_text())
assert page.headings == 1
assert len(page.ids) == len(set(page.ids))
assert page.canonical == page.metas['og:url'] == site_url
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
assert len(apps) == 6
for app in apps:
    assert app['url'] in page.links or app['url'] == app['@id'], app['name']
    assert app['@id'].split('#')[1] in page.ids
    assert app['name'] in Path('llms.txt').read_text()
    assert not any(key in app for key in ('aggregateRating', 'offers', 'review'))
robot = RobotFileParser()
robot.parse(Path('robots.txt').read_text().splitlines())
for agent in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'PerplexityBot'):
    assert robot.can_fetch(agent, page.canonical), agent
locs = ET.parse('sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
assert [loc.text for loc in locs] == [page.canonical, site_url + 'apps/privacy/', site_url + 'work-with-me/']
print('Passed: metadata, canonical, six linked app entities, schema references, local images, section anchors, sitemap, and crawler access.')

privacy_path = Path('apps/privacy/index.html')
privacy = Page()
privacy.feed(privacy_path.read_text())
assert privacy.headings == 1
assert len(privacy.ids) == len(set(privacy.ids))
assert privacy.canonical == site_url + 'apps/privacy/'
assert 'noindex' not in privacy.metas['robots']
for link in privacy.links:
    if link.startswith('#'): assert link[1:] in privacy.ids, link
for path in privacy.images: assert (privacy_path.parent / path).is_file(), path
assert Path('apps/privacy/privacy.css').is_file()
assert 'apps/privacy/' in page.links
for identifier in ('TangCai Invest AB', 'SnusTracker', 'info@tangcai.se'):
    assert identifier in privacy_path.read_text(), identifier
print('Passed: privacy page identity, canonical, headings, anchors, assets, and homepage link.')

profile_path = Path('work-with-me/index.html')
profile = Page()
profile.feed(profile_path.read_text())
assert profile.headings == 1
assert len(profile.ids) == len(set(profile.ids))
assert profile.canonical == profile.metas['og:url'] == site_url + 'work-with-me/'
assert 'noindex' not in profile.metas['robots']
profile_nodes = json.loads(profile.schema)['@graph']
node_ids = {node['@id'] for node in profile_nodes}
assert len(node_ids) == len(profile_nodes)
check_refs(profile_nodes)
by_type = {node['@type']: node for node in profile_nodes}
assert {'Person', 'Organization', 'WebSite', 'WebPage', 'Service', 'BreadcrumbList'} <= by_type.keys()
assert by_type['Person']['name'] == 'Xiaoming'
assert by_type['Service']['provider']['@id'] == site_url + '#organization'
assert by_type['WebPage']['url'] == profile.canonical
assert by_type['WebPage']['mainEntity']['@id'] == by_type['Service']['@id']
assert by_type['BreadcrumbList']['itemListElement'][-1]['item'] == profile.canonical
for node in profile_nodes:
    assert not any(key in node for key in ('aggregateRating', 'review', 'offers'))
for key in ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt'):
    assert profile.metas.get(key), key
assert profile.metas['twitter:title'] == profile.metas['og:title']
assert 'questions' in profile.ids
assert profile.canonical in Path('llms.txt').read_text()
for agent in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'PerplexityBot'):
    assert robot.can_fetch(agent, profile.canonical), agent
assert 'work-with-me/' in page.links
assert Path('work-with-me/profile.css').is_file()
for path in profile.images: assert (profile_path.parent / path).is_file(), path
for link in profile.links:
    if link.startswith('#'): assert link[1:] in profile.ids, link
    elif link.startswith('../'):
        target, _, fragment = link.partition('#')
        resolved = profile_path.parent / target
        if resolved.is_dir(): resolved = resolved / 'index.html'
        assert resolved.is_file(), link
        if fragment:
            destination = Page()
            destination.feed(resolved.read_text())
            assert fragment in destination.ids, link
assert any(link.startswith('mailto:info@tangcai.se?subject=Work%20with%20Xiaoming') for link in profile.links)
print('Passed: profile metadata, schema, headings, assets, navigation, portfolio anchors, and enquiry link.')
