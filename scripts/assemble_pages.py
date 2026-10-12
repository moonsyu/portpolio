"""Publish web/app main at the root and the full portfolio below /embedded/."""
import argparse
import json
import re
import shutil
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit


SITE_URL = 'https://moonsyu.github.io/portpolio/'
PUBLIC_FILES = ('index.html', 'styles.css', 'app.js', '.nojekyll')
PUBLIC_FOLDERS = ('assets',)
PDF_FILES = {'main': 'Jang-MoonSu-Web-App-Portfolio.pdf',
             'embedded': 'Jang-MoonSu-Portfolio.pdf'}


class LocalReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.downloads = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'a' and 'button-pdf' in attributes.get('class', '').split():
            self.downloads.append(attributes.get('href', ''))
        for name, value in attrs:
            if value and name in ('src', 'href', 'data-gif', 'data-poster'):
                self.urls.append(value)


def validate_references(destination, branch):
    parser = LocalReferences()
    parser.feed((destination / 'index.html').read_text(encoding='utf-8'))
    if len(parser.downloads) != 1 or urlsplit(parser.downloads[0]).path != './output/pdf/' + PDF_FILES[branch]:
        raise ValueError(f'{branch} must link only its matching PDF')
    missing = []
    for url in parser.urls:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        target = (destination / unquote(parts.path)).resolve()
        if not target.is_relative_to(destination) or not target.is_file():
            missing.append(url)
    if missing:
        raise ValueError(f'Missing or non-local page resources: {missing}')


def source_revision(source):
    return subprocess.check_output(
        ['git', '-C', str(source), 'rev-parse', 'HEAD'], text=True
    ).strip()


def copy_site(source, destination, branch, url):
    destination.mkdir(parents=True, exist_ok=True)
    for relative in (*PUBLIC_FILES, *PUBLIC_FOLDERS, 'output/pdf/' + PDF_FILES[branch]):
        item = source / relative
        if not item.exists():
            raise FileNotFoundError(item)
        if item.is_symlink() or (item.is_dir() and any(p.is_symlink() for p in item.rglob('*'))):
            raise ValueError(f'Symlink cannot be published: {relative}')
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copyfile(item, target)
    html_path = destination / 'index.html'
    html = html_path.read_text(encoding='utf-8')
    # Relative assets and fragment links already work at either mount point.
    for pattern in (
        r'(<link\b[^>]*\brel="canonical"[^>]*\bhref=")[^"]*(")',
        r'(<meta\b[^>]*\bproperty="og:url"[^>]*\bcontent=")[^"]*(")',
    ):
        html, count = re.subn(pattern, lambda m: m[1] + url + m[2], html)
        if count != 1:
            raise ValueError(f'Expected one canonical/social URL in {branch}')
    html_path.write_text(html, encoding='utf-8')
    validate_references(destination, branch)
    metadata = {'branch': branch, 'commit': source_revision(source), 'url': url}
    (destination / 'deployment.json').write_text(
        json.dumps(metadata, indent=2) + '\n', encoding='utf-8'
    )
    return metadata


def assemble(main, embedded, output):
    main, embedded, output = (Path(p).resolve() for p in (main, embedded, output))
    if main == embedded:
        raise ValueError('Use separate checkouts for main and embedded')
    if any(output == source or output.is_relative_to(source) or source.is_relative_to(output)
           for source in (main, embedded)):
        raise ValueError('Output must be separate from both source checkouts')
    if output.exists() and any(output.iterdir()):
        raise ValueError('Output must be empty; existing files are never deleted')
    output.mkdir(parents=True, exist_ok=True)
    return [copy_site(main, output, 'main', SITE_URL),
            copy_site(embedded, output / 'embedded', 'embedded', urljoin(SITE_URL, 'embedded/'))]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main', required=True, type=Path)
    parser.add_argument('--embedded', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(assemble(args.main, args.embedded, args.output), indent=2))
