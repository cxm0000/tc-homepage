"""Package only public assets and use the deployment's actual canonical URL."""
import argparse
from pathlib import Path
import shutil
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('--site-url', required=True)
args = parser.parse_args()
site_url = args.site_url.rstrip('/') + '/'
parsed = urlparse(site_url)
assert parsed.scheme == 'https' and parsed.netloc and not parsed.query and not parsed.fragment
output = Path('_site')
output.mkdir(exist_ok=True)
for filename in ('index.html', 'styles.css', 'logo.png', 'robots.txt', 'sitemap.xml', 'llms.txt'):
    source = Path(filename)
    if source.suffix in ('.html', '.txt', '.xml'):
        (output / filename).write_text(source.read_text().replace('https://tangcai.se/', site_url))
    else:
        shutil.copy2(source, output / filename)
shutil.copytree('assets', output / 'assets', dirs_exist_ok=True)
(output / '.nojekyll').touch()
print(f'Packaged public homepage for {site_url}')
