import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('iv4_lookup', ROOT / 'skills/keyence-iv4/scripts/lookup.py')
lookup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lookup)


class LookupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.skill = root / 'skill'
        refs = self.skill / 'references'
        refs.mkdir(parents=True)
        (refs / 'hardware.md').write_text('IV4-H sensor trigger details', encoding='utf-8')
        self.write(refs / 'commands.json', {'commands': [{'id': 'CMD-T1', 'code': 'T1', 'family': 'IV4-H', 'source_id': 'iv4_1234567890abcdef', 'pdf_page': 2}, {'code': 'T2', 'family': 'IV4-H'}]})
        self.write(refs / 'sources.json', {'sources': [{'source_id': 'iv4_1234567890abcdef', 'filename': 'manual.pdf', 'pages': 3}]})
        self.write(refs / 'descriptors.json', {'descriptors': [{'identity': 'GSDML test'}]})
        self.corpus = root / 'corpus'
        knowledge = self.corpus / 'knowledge'
        knowledge.mkdir(parents=True)
        self.write(knowledge / '00_KNOWLEDGE_INDEX.json', {'sources': [{'source_id': 'iv4_1234567890abcdef', 'sha256': 'a' * 64, 'pages': 3, 'pages_index': [{'pdf_page': i} for i in (1, 2, 3)]}]})
        (knowledge / 'A_IV4_Hardware.md').write_text(''.join(f'## iv4_1234567890abcdef · PDF p. {i} · section\nIV4-H trigger page {i}\n' for i in (1, 2, 3)), encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, path, value):
        path.write_text(json.dumps(value), encoding='utf-8')

    def test_standalone_and_exact_command(self):
        self.assertEqual(lookup.lookup(skill=self.skill, status=True)['mode'], 'standalone')
        self.assertEqual(lookup.lookup(skill=self.skill, command='t1')['results'], [{'id': 'CMD-T1', 'code': 'T1', 'family': 'IV4-H', 'source_id': 'iv4_1234567890abcdef', 'pdf_page': 2}])
        self.assertEqual(lookup.lookup(skill=self.skill, command='T')['results'], [])
        self.assertEqual(lookup.lookup(skill=self.skill, query='trigger')['results'][0]['id'], 'REF-hardware')
        self.assertEqual(lookup.lookup(skill=self.skill, address='iv4_1234567890abcdef')['source']['filename'], 'manual.pdf')
        self.assertTrue(lookup.lookup(skill=self.skill, descriptor='GSDML')['results'])
        self.assertEqual(lookup.lookup(skill=self.skill, query='T1')['results'][0]['id'], 'CMD-T1')
        public = lookup.lookup(skill=self.skill, address='iv4_1234567890abcdef:p0002')
        self.assertFalse(public['full_page_available'])
        self.assertEqual(public['records'][0]['id'], 'CMD-T1')
        self.assertTrue(lookup.lookup(skill=self.skill, command='T1', maximum=10)['results'][0]['truncated'])

    def test_optional_corpus_pages_neighbors_and_bounds(self):
        knowledge = self.corpus / 'knowledge'
        (knowledge / 'A_IV4_Hardware.md').write_text('## iv4_1234567890abcdef · PDF p. 3 · section\nIV4-H trigger page 3\n', encoding='utf-8')
        (knowledge / 'B_IV4_Configuration.md').write_text(''.join(f'## iv4_1234567890abcdef · PDF p. {i} · section\nIV4-H trigger page {i}\n' for i in (1, 2)), encoding='utf-8')
        result = lookup.lookup(skill=self.skill, corpus=self.corpus, address='iv4_1234567890abcdef:p0002', neighbors=1, maximum=20)
        self.assertEqual([x['id'][-1] for x in result['results']], ['1', '2', '3'])
        self.assertTrue(all(len(x['text']) <= 20 for x in result['results']))
        self.assertTrue(any(x['id'].endswith('p0002') for x in lookup.lookup(skill=self.skill, corpus=self.corpus, query='page 2', literal=True)['results']))
        with self.assertRaises(ValueError):
            lookup.lookup(skill=self.skill, corpus=self.corpus / 'missing', status=True)

    def test_optional_research_facts_are_not_pages_or_private_catalog(self):
        refs = self.skill / 'references'
        fact = {'id': 'RT-SHARED', 'family': 'IV4', 'firmware': 'R1.30.02',
                'evidence_category': 'VERIFIED_RUNTIME', 'statement': 'recognized text differs master',
                'source_locators': ['IV4_RESEARCH_V2/docs/OCR_RUNTIME.md']}
        self.write(refs / 'runtime-observations.json', {'observations': [fact]})
        self.write(self.corpus / 'knowledge/IV4_RESEARCH_FACTS.json',
                   {'facts': [fact, {**fact, 'id': 'IV4-RESEARCH-OCR'}],
                    'sources': [{'local_root': 'PRIVATE_HOST_ROOT'}]})
        result = lookup.lookup(skill=self.skill, corpus=self.corpus, query='recognized', firmware='R1.30.02')
        self.assertEqual([x['id'] for x in result['results']], ['RT-SHARED', 'IV4-RESEARCH-OCR'])
        exact = lookup.lookup(skill=self.skill, corpus=self.corpus, address='IV4-RESEARCH-OCR')
        self.assertEqual(exact['record']['firmware'], 'R1.30.02')
        self.assertNotIn('PRIVATE_HOST_ROOT', json.dumps(exact))
        self.assertNotIn('full_page_available', exact)
        self.assertEqual(lookup.lookup(skill=self.skill, corpus=self.corpus, query='recognized', firmware='R1.20.05')['results'], [])
        with self.assertRaises(ValueError):
            lookup.lookup(skill=self.skill, address='RT-SHARED', family='IV4-H')

    def test_evidence_page_selection(self):
        doc = self.corpus / 'evidence/fast/documents/hash'
        doc.mkdir(parents=True)
        self.write(doc / 'source_record.json', {'source_sha256': 'a' * 64})
        (doc / 'table_index.jsonl').write_text(json.dumps({'pdf_page': 2, 'rows': [['T1', 'trigger']], 'table_type': 'command'}) + '\n', encoding='utf-8')
        (doc / 'page_index.jsonl').write_text(json.dumps({'pdf_page': 2, 'text': 'target', 'path': 'private'}) + '\n' + json.dumps({'pdf_page': 3, 'text': 'other'}) + '\n', encoding='utf-8')
        result = lookup.lookup(skill=self.skill, corpus=self.corpus, address='iv4_1234567890abcdef:p0002', include_evidence=True)
        self.assertEqual(len(result['evidence']), 2)
        self.assertIn('trigger', json.dumps(result['evidence']))
        self.assertNotIn('private', json.dumps(result))
        self.write(doc / 'source_record.json', {'source_sha256': 'a' * 63 + 'b', 'note': 'a' * 64})
        rejected = lookup.lookup(skill=self.skill, corpus=self.corpus, address='iv4_1234567890abcdef:p0002', include_evidence=True)
        self.assertEqual(rejected['evidence'], [])


class ActualRegistryIntegration(unittest.TestCase):
    def test_runtime_firmware_boundaries_and_facts(self):
        result = lookup.lookup(query='ITR', firmware='R1.20.05', maximum=10000)
        self.assertTrue(result['results'])
        self.assertTrue(all(x['firmware'] == 'R1.20.05' for x in result['results']))
        self.assertIn('ER02', json.dumps(result))
        newer = lookup.lookup(query='ITR', firmware='R1.30.02', maximum=10000)
        self.assertIn('ER22', json.dumps(newer))
        self.assertEqual(lookup.lookup(query='OCR', family='IV4-H', firmware='R1.30.02')['results'], [])
        ocr = lookup.lookup(address='RT-IV4-R13002-OCR', maximum=10000)['record']
        self.assertEqual(ocr['model'], 'IV4-500CA')
        self.assertIn('confidence', json.dumps(ocr))
        self.assertIn('7223', json.dumps(ocr))
        ftp = lookup.lookup(address='RT-IV4-R13002-FTP', maximum=10000)['record']
        self.assertIn('8/9', json.dumps(ftp))
        self.assertIn('000', json.dumps(ftp))
        self.assertTrue(ftp['limitations'])
        with self.assertRaises(ValueError):
            lookup.lookup(address='RT-IV4-R13002-OCR', firmware='R1.20.05')
        with self.assertRaises(ValueError):
            lookup.lookup(command='RT', firmware='R1.30.02')

    def test_runtime_registry_identity_and_sanitized_logical_sources(self):
        import re
        data = json.loads((ROOT / 'skills/keyence-iv4/references/runtime-observations.json').read_text(encoding='utf-8'))
        self.assertFalse(data['production_accepted'])
        records = data['observations']
        self.assertEqual(len({r['id'] for r in records}), len(records))
        self.assertEqual({r['firmware'] for r in records}, {'R1.20.05', 'R1.30.02'})
        for record in records:
            self.assertEqual(record['family'], 'IV4')
            self.assertTrue(record['observed'])
            self.assertTrue(record['limitations'])
            self.assertTrue(record['source_locators'])
            for locator in record['source_locators']:
                self.assertRegex(locator, r'^IV4_RESEARCH(?:_V2)?/(?:docs|evidence)/[^:]+$')
                self.assertNotIn('..', locator)
        self.assertIsNone(re.search(r'(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])', json.dumps(data).replace('2.10.01.0', 'NAVIGATOR_VERSION')))

    def test_actual_registry_contract_when_present(self):
        refs = ROOT / 'skills/keyence-iv4/references'
        required = [refs / name for name in ('sources.json', 'commands.json', 'capabilities.json')]
        if not all(path.is_file() for path in required):
            self.skipTest('Root registry files are still being authored')
        commands = json.loads((refs / 'commands.json').read_text(encoding='utf-8-sig'))['commands']
        self.assertTrue(commands)
        first = commands[0]
        found = lookup.lookup(command=first['code'], family=first.get('family'))
        self.assertTrue(any(item.get('id') == first['id'] for item in found['results']))
        self.assertEqual(lookup.lookup(address=first['id'])['id'], first['id'])
        self.assertTrue(lookup.lookup(query=first['code'])['results'])


if __name__ == '__main__':
    unittest.main()
