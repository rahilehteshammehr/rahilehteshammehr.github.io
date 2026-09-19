#!/usr/bin/env python3
"""Regression tests for source selection and preservation; no extra dependencies."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from prepare_cv import prepare


class CVSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for folder in ('_data', 'cv-source', 'files', 'scripts', '.cache'):
            (self.root / folder).mkdir()
        self.config = {'mode': 'auto', 'manual_file': 'cv-source/manual.pdf',
                       'published_file': '/files/CV.pdf'}
        self.manual = self.root / 'cv-source/manual.pdf'
        self.manual.write_bytes(b'%PDF-1.4\nmanual fixture')
        self.output = self.root / 'files/CV.pdf'
        self.output.write_bytes(b'%PDF-1.4\nprevious published fixture')
        (self.root / 'scripts/build_cv.py').write_text(
            'from pathlib import Path\n'
            'root = Path(__file__).resolve().parents[1]\n'
            '(root / ".cache/generated-cv.pdf").write_bytes(b"%PDF-1.4\\nauto fixture")\n')

    def run_prepare(self):
        (self.root / '_data/cv_pdf.json').write_text(json.dumps(self.config))
        with contextlib.redirect_stdout(io.StringIO()):
            prepare(self.root)

    def test_switch_auto_manual_auto_preserves_source_and_url(self):
        original = self.manual.read_bytes()
        self.run_prepare()
        self.assertEqual(self.output.read_bytes(), b'%PDF-1.4\nauto fixture')
        self.config['mode'] = 'manual'
        self.run_prepare()
        self.assertEqual(self.output.read_bytes(), original)
        self.config['mode'] = 'auto'
        self.run_prepare()
        self.assertEqual(self.output.read_bytes(), b'%PDF-1.4\nauto fixture')
        self.assertEqual(self.manual.read_bytes(), original)

    def test_manual_mode_does_not_run_generator(self):
        (self.root / 'scripts/build_cv.py').write_text('raise RuntimeError("Must not run")')
        self.config['mode'] = 'manual'
        self.run_prepare()
        self.assertEqual(self.output.read_bytes(), self.manual.read_bytes())
        self.assertFalse((self.root / '.cache/generated-cv.pdf').exists())

    def test_missing_manual_stops_without_overwriting_output(self):
        self.config['mode'] = 'manual'
        self.manual.unlink()
        previous = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Manual CV not found'):
            self.run_prepare()
        self.assertEqual(self.output.read_bytes(), previous)

    def test_non_pdf_stops_without_overwriting_output(self):
        self.config['mode'] = 'manual'
        self.manual.write_text('LaTeX or other non-PDF content')
        previous = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, 'not a PDF file'):
            self.run_prepare()
        self.assertEqual(self.output.read_bytes(), previous)

    def test_invalid_mode_does_not_fall_back(self):
        self.config['mode'] = 'manul'
        previous = self.output.read_bytes()
        with self.assertRaisesRegex(ValueError, 'mode must be'):
            self.run_prepare()
        self.assertEqual(self.output.read_bytes(), previous)

    def test_source_and_output_cannot_escape_their_folders(self):
        for field, path in [('manual_file', 'cv-source/../files/CV.pdf'),
                            ('published_file', '/files/../cv-source/manual.pdf')]:
            with self.subTest(field=field):
                saved = self.config[field]
                self.config[field] = path
                with self.assertRaisesRegex(ValueError, 'must stay inside'):
                    self.run_prepare()
                self.config[field] = saved

    def test_replacing_manual_pdf_is_picked_up(self):
        self.config['mode'] = 'manual'
        self.run_prepare()
        self.manual.write_bytes(b'%PDF-1.4\nupdated manual fixture')
        self.run_prepare()
        self.assertEqual(self.output.read_bytes(), self.manual.read_bytes())


if __name__ == '__main__':
    unittest.main()
