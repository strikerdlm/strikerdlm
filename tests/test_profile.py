"""Offline checks: python -m unittest discover -s tests -v. No Actions needed."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []
        self.alts = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('img', 'source'):
            self.paths.append(attrs.get('src') or attrs.get('srcset', ''))
        if tag == 'img':
            self.alts.append(attrs.get('alt', ''))

class ProfileTests(unittest.TestCase):
    def setUp(self):
        path = ROOT / 'README.md'
        self.assertTrue(path.is_file(), 'The profile README must exist')
        self.text = path.read_text(encoding='utf-8')

    def test_no_workflows(self):
        workflows = ROOT / '.github' / 'workflows'
        self.assertFalse(list(workflows.glob('*.yml')) + list(workflows.glob('*.yaml')))

    def test_local_images_with_alt_text(self):
        parser = Images()
        parser.feed(self.text)
        self.assertTrue(parser.paths)
        self.assertTrue(parser.alts)
        self.assertTrue(all(alt.strip() for alt in parser.alts))
        for path in parser.paths:
            self.assertFalse(re.match(r'^(?:[a-z]+:)?//', path, re.I), path)
            target = (ROOT / path).resolve()
            self.assertTrue(target.is_relative_to(ROOT.resolve()), path)
            self.assertTrue(target.is_file(), path)
        self.assertNotRegex(self.text, r'!\[[^\]]*\]\(https?://')

    def test_svg_is_static_and_self_contained(self):
        assets = list((ROOT / 'assets').glob('*.svg'))
        self.assertEqual(len(assets), 2)
        forbidden = {'script', 'foreignObject', 'image', 'animate', 'animateTransform', 'set', 'a'}
        for path in assets:
            root = ET.fromstring(path.read_text(encoding='utf-8'))
            self.assertIn('viewBox', root.attrib)
            self.assertTrue(root.find('{http://www.w3.org/2000/svg}title') is not None)
            for node in root.iter():
                self.assertNotIn(node.tag.split('}')[-1], forbidden)
                for key, value in node.attrib.items():
                    self.assertFalse(key.lower().startswith('on'))
                    self.assertNotRegex(value, r'https?://|javascript:|@import')
                    if key.split('}')[-1] == 'href':
                        self.assertTrue(value.startswith('#'))

    def test_curated_projects_are_unique(self):
        # Visibility and descriptions were checked through GitHub on 2026-09-11.
        # This offline test prevents duplication; it cannot recheck live visibility.
        projects = re.findall(r'https://github\.com/strikerdlm/([\w.-]+)', self.text)
        expected = {'OpenMATB', 'hexoskin-wav-analyzer', 'ROBD2_GUI', 'meteor'}
        self.assertEqual(set(projects), expected)
        self.assertEqual(len(projects), len(expected))
        self.assertIn('Public fork', self.text)
        self.assertIn('Experimental', self.text)

    def test_no_legacy_widgets_or_fake_counts(self):
        for term in ('shields.io', 'vercel.app', 'demolab.com', 'komarev.com',
                     'github-metrics.svg', 'profile-3d-contrib', 'snake',
                     'count_private', 'Repos-49', 'HumanPerformanceCalcs'):
            self.assertNotIn(term, self.text)
        self.assertLess(len(self.text.encode('utf-8')), 5000)

    def test_native_text_and_contacts(self):
        self.assertEqual(len(re.findall(r'^# ', self.text, re.M)), 1)
        self.assertIn('Diego L. Malpica, MD', self.text)
        self.assertIn('mailto:dlmalpica@me.com', self.text)
        self.assertIn('https://orcid.org/0000-0002-2257-4940', self.text)
        self.assertNotRegex(self.text, r'<(?:script|style|iframe)\b')
        self.assertEqual(self.text.count('<details>'), self.text.count('</details>'))
        self.assertEqual(self.text.count('<picture>'), self.text.count('</picture>'))

if __name__ == '__main__':
    unittest.main()
