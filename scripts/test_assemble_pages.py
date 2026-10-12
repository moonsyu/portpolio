"""Check branch isolation, URL mounting, resource availability and output safety."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from assemble_pages import PDF_FILES, SITE_URL, assemble


class BranchSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.main = self.root / 'main'
        self.embedded = self.root / 'embedded'
        self.output = self.root / 'published'
        for directory, title in ((self.main, 'MAIN'), (self.embedded, 'EMBEDDED')):
            (directory / 'assets').mkdir(parents=True)
            (directory / 'output/pdf').mkdir(parents=True)
            (directory / 'docs').mkdir()
            (directory / 'docs/private.md').write_text('not a site asset')
            (directory / '.env').write_text('not a site asset')
            (directory / 'index.html').write_text(
                f'<link rel="canonical" href="{SITE_URL}">'
                f'<meta property="og:url" content="{SITE_URL}">'
                f'<h1>{title}</h1><img src="./assets/screen.png?v=1">'
                f'<a class="button-pdf" href="./output/pdf/{PDF_FILES[title.lower()]}">PDF</a><a href="#about">About</a>',
                encoding='utf-8',
            )
            for name in ('styles.css', 'app.js', '.nojekyll', 'assets/screen.png', 'output/pdf/' + PDF_FILES[title.lower()]):
                (directory / name).write_text(title)
        revision = patch('assemble_pages.source_revision', side_effect=lambda p: p.name + '-sha')
        revision.start()
        self.addCleanup(revision.stop)

    def test_branches_keep_independent_content_and_files(self):
        assemble(self.main, self.embedded, self.output)
        for mount, title, url in ((self.output, 'MAIN', SITE_URL),
                                  (self.output / 'embedded', 'EMBEDDED', SITE_URL + 'embedded/')):
            self.assertIn(f'<h1>{title}</h1>', (mount / 'index.html').read_text())
            self.assertIn(f'rel="canonical" href="{url}"', (mount / 'index.html').read_text())
            self.assertIn(f'property="og:url" content="{url}"', (mount / 'index.html').read_text())
            self.assertEqual((mount / 'assets/screen.png').read_text(), title)
            self.assertEqual((mount / 'output/pdf' / PDF_FILES[title.lower()]).read_text(), title)
            self.assertFalse((mount / '.env').exists())
            self.assertFalse((mount / 'docs').exists())
            self.assertEqual(json.loads((mount / 'deployment.json').read_text())['branch'], title.lower())
        self.assertNotIn(SITE_URL + 'embedded/', (self.embedded / 'index.html').read_text())

    def test_missing_branch_resource_stops_publication(self):
        (self.embedded / 'assets/screen.png').unlink()
        with self.assertRaisesRegex(ValueError, 'Missing'):
            assemble(self.main, self.embedded, self.output)

    def test_wrong_pdf_mapping_stops_publication(self):
        page = self.main / 'index.html'
        page.write_text(page.read_text().replace(PDF_FILES['main'], PDF_FILES['embedded']))
        with self.assertRaisesRegex(ValueError, 'matching PDF'):
            assemble(self.main, self.embedded, self.output)

    def test_existing_output_is_preserved(self):
        self.output.mkdir()
        marker = self.output / 'keep.txt'
        marker.write_text('keep')
        with self.assertRaisesRegex(ValueError, 'empty'):
            assemble(self.main, self.embedded, self.output)
        self.assertEqual(marker.read_text(), 'keep')

    def test_output_cannot_overwrite_sources(self):
        with self.assertRaisesRegex(ValueError, 'separate'):
            assemble(self.main, self.embedded, self.main / 'published')


if __name__ == '__main__':
    unittest.main()
