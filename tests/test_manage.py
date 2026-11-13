import importlib.util
import json
import os
import subprocess
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('iv4_manage', ROOT / 'tools/manage.py')
manage = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manage)


class ManageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.source = root / 'source'
        refs = self.source / 'references'
        refs.mkdir(parents=True)
        (self.source / 'SKILL.md').write_text('---\nname: keyence-iv4\ndescription: test\n---\n[hardware](references/hardware.md)\n', encoding='utf-8')
        (refs / 'hardware.md').write_text('test', encoding='utf-8')
        for name in ('sources', 'commands', 'capabilities'):
            (refs / (name + '.json')).write_text('{}', encoding='utf-8')
        self.parent = root / 'skills'

    def tearDown(self):
        self.tmp.cleanup()

    def test_install_update_modified_uninstall(self):
        target = manage.install(self.parent, self.source)
        self.assertEqual(manage.status(self.parent)['existing'][0]['state'], 'managed')
        (self.source / 'references/hardware.md').write_text('updated', encoding='utf-8')
        manage.install(self.parent, self.source)
        self.assertEqual((target / 'references/hardware.md').read_text(encoding='utf-8'), 'updated')
        (target / 'references/hardware.md').write_text('local edit', encoding='utf-8')
        with self.assertRaises(ValueError):
            manage.install(self.parent, self.source)
        with self.assertRaises(ValueError):
            manage.uninstall(self.parent)
        (target / 'references/hardware.md').write_text('updated', encoding='utf-8')
        manage.uninstall(self.parent)
        self.assertFalse(target.exists())

    def test_foreign_collision(self):
        target = self.parent / 'keyence-iv4'
        target.mkdir(parents=True)
        (target / 'user.txt').write_text('keep')
        with self.assertRaises(ValueError):
            manage.install(self.parent, self.source)
        with self.assertRaises(ValueError):
            manage.uninstall(self.parent)
        self.assertEqual((target / 'user.txt').read_text(), 'keep')

    def test_validate_broken_link(self):
        (self.source / 'SKILL.md').write_text('---\nname: keyence-iv4\ndescription: test\n---\n[bad](missing.md)', encoding='utf-8')
        with self.assertRaises(ValueError):
            manage.validate(self.source)

    def test_reparse_point_rejected(self):
        outside = Path(self.tmp.name) / 'outside'
        outside.mkdir()
        link = self.parent / 'keyence-iv4'
        self.parent.mkdir()
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(outside)], capture_output=True)
            if result.returncode:
                try:
                    link.symlink_to(outside, target_is_directory=True)
                except OSError:
                    self.skipTest('Cannot create junction or symlink on this host')
        else:
            link.symlink_to(outside, target_is_directory=True)
        self.assertTrue(manage.is_link(link))
        with self.assertRaises(ValueError):
            manage.install(self.parent, self.source)
        with self.assertRaises(ValueError):
            manage.uninstall(self.parent)

    def test_frontmatter_and_yaml(self):
        agents = self.source / 'agents'
        agents.mkdir()
        (agents / 'openai.yaml').write_text('interface:\n  display_name: IV4\n', encoding='utf-8')
        manage.validate(self.source)
        (self.source / 'SKILL.md').write_text('---\nname: keyence-iv4\ndescription: test\nmissing close', encoding='utf-8')
        with self.assertRaises(ValueError):
            manage.validate(self.source)


if __name__ == '__main__':
    unittest.main()
