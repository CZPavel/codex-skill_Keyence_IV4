import json,subprocess,sys,tempfile,importlib.util
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1];SKILL=ROOT/'skills/keyence-iv4'
spec=importlib.util.spec_from_file_location('manager',ROOT/'tools/manage.py');manage=importlib.util.module_from_spec(spec);spec.loader.exec_module(manage)
class KnowledgeTests(unittest.TestCase):
 def test_model_bound_command_inventory_and_anomalies(self):
  data=json.loads((SKILL/'references/commands.json').read_text(encoding='utf-8'))['commands'];self.assertEqual(sum(c['family']=='IV4' for c in data),43);self.assertEqual(sum(c['family']=='IV4-H' for c in data),46);self.assertEqual(len({c['id'] for c in data}),89)
  for c in data:
   self.assertTrue(c['parameters'] or c['code'] in {'T1','T2','RT','MR','WC','SDS','CTR','CTU','MC'});self.assertLessEqual(c['detail_pdf_page'],632);self.assertTrue(c['source_document'].endswith('.pdf'))
  h=next(c for c in data if c['id']=='CMD-IV4-H-CSR');self.assertEqual(h['wire_status'],'REVIEW_REQUIRED');self.assertTrue(h['anomalies'])
  h=next(c for c in data if c['id']=='CMD-IV4-H-OF');self.assertTrue(any('OF04' in p and 'Disable' in p for p in h['preconditions']))
  self.assertFalse(any(c['family']=='IV4' and c['code'] in ['MC','DWC','DRC'] for c in data))
 def test_provenance_and_descriptor_scope(self):
  sources=json.loads((SKILL/'references/sources.json').read_text(encoding='utf-8'))['sources'];self.assertEqual(len(sources),15)
  for s in sources:self.assertEqual(s['source_id'],'iv4_'+s['sha256'][:16]);self.assertGreater(s['pages'],0)
  ds=json.loads((SKILL/'references/descriptors.json').read_text(encoding='utf-8'))['descriptors'];self.assertEqual(len(ds),4);self.assertTrue(all(d['classification']=='DESCRIPTOR_ONLY' for d in ds));self.assertEqual(sum(len(d.get('modules',[])) for d in ds),33)
 def test_real_distribution_without_private_sources(self):
  with tempfile.TemporaryDirectory() as temp:
   target=manage.install(Path(temp)/'skills')
   proc=subprocess.run([sys.executable,'-I','-S',str(target/'scripts/lookup.py'),'--command','CSR','--family','IV4-H','--max-chars','5000'],cwd=temp,capture_output=True,text=True,encoding='utf-8',check=True)
   result=json.loads(proc.stdout);self.assertEqual(result['total_matches'],1);self.assertIn('REVIEW_REQUIRED',proc.stdout)
   # Original manual page is not pretended to be present in standalone mode.
   proc=subprocess.run([sys.executable,'-I','-S',str(target/'scripts/lookup.py'),'--id','iv4_f2b18663143f7e12:p0505'],cwd=temp,capture_output=True,text=True,encoding='utf-8',check=True);self.assertIn('standalone-limited',proc.stdout)
   manage.uninstall(Path(temp)/'skills')
 def test_behavior_answers_are_actual_recorded_runs(self):
  scenarios=json.loads((ROOT/'tests/scenarios.json').read_text(encoding='utf-8'));answers=json.loads((ROOT/'docs/behavior-answers.json').read_text(encoding='utf-8'));self.assertTrue(answers['skill_loaded']);self.assertEqual({s['id'] for s in scenarios},{a['id'] for a in answers['answers']});self.assertTrue(answers['lookup_commands_executed'])
if __name__=='__main__':unittest.main()
