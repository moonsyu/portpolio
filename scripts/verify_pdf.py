"""Reject missing text/pages/local links, then add PDF metadata and bookmarks."""
import json
import re
import sys
import unicodedata
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def normalize(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text))


def verify(pdf_path, layout_path):
    report = json.loads(layout_path.read_text(encoding='utf-8'))
    reader = PdfReader(pdf_path)
    assert len(reader.pages) == len(report['slides']), 'Unexpected PDF page count'
    failures = []
    for number, (page, source) in enumerate(zip(reader.pages, report['layout']), 1):
        text = page.extract_text()
        normalized = normalize(text)
        if '\ufffd' in text:
            failures.append(f'Page {number}: invalid text encoding')
        for expected in source['text']:
            if normalize(expected) not in normalized:
                failures.append(f'Page {number}: missing text {expected!r}')
        box = page.mediabox
        if abs(float(box.width) / float(box.height) - 16 / 9) > 0.003:
            failures.append(f'Page {number}: not widescreen')
        for annotation in page.get('/Annots', []):
            uri = annotation.get_object().get('/A', {}).get('/URI', '')
            if uri and not uri.startswith(('https://', 'mailto:')):
                failures.append(f'Page {number}: non-public link')
    if failures:
        raise ValueError('\n'.join(failures))
    writer = PdfWriter(clone_from=reader)
    writer.add_metadata({'/Author': 'Jang MoonSu', '/Subject': 'Developer Portfolio'})
    for number, slide in enumerate(report['slides']):
        writer.add_outline_item(slide['title'], number)
    temporary = pdf_path.with_suffix('.verified.pdf')
    with temporary.open('wb') as output:
        writer.write(output)
    temporary.replace(pdf_path)
    final = PdfReader(pdf_path)
    assert len(final.pages) == len(reader.pages)
    assert all(normalize(a.extract_text()) == normalize(b.extract_text())
               for a, b in zip(reader.pages, final.pages))
    print(f'Verified {len(final.pages)} pages: all source text retained; public links only')


if __name__ == '__main__':
    verify(Path(sys.argv[1]), Path(sys.argv[2]))
