import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/'skills/keyence-iv4/scripts/wire_contract.py'
spec=importlib.util.spec_from_file_location('wire',P);w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)
class WireTests(unittest.TestCase):
 def test_partial_coalesced_ack_result(self):
  b=w.CRFrames();self.assertEqual(b.feed(b'T'),[]);self.assertEqual(b.feed(b'1\rRT,000'),[b'T1\r']);frames=b.feed(b'31,OK,01,OK,0000091\r');self.assertEqual(w.parse_rt_standard(frames[0],mode='standard')['counter'],31)
 def test_reject_mixed_binary_and_overflow(self):
  with self.assertRaises(ValueError):w.CRFrames().feed(b'BR,0000000031,0000003,A\rB')
  with self.assertRaises(ValueError):w.CRFrames(4).feed(b'ABCDE')
 def test_invalid_result_not_OK(self):
  result=w.parse_rt_standard(b'RT,00031,OK,01,--,0000000\r',mode='standard');self.assertFalse(result['decidable'])
 def test_reject_wrong_contract_and_duplicate(self):
  for mode,fmt,data in [('count','00',b'RT,00031,OK,01,OK,0000091\r'),('standard','01',b'RT,00031,OK,01,OK,0000091\r'),('standard','00',b'RT,00031,OK,01,OK,0000091,01,OK,0000091\r')]:
   with self.assertRaises(ValueError):w.parse_rt_standard(data,mode=mode,output_format=fmt)
 def test_error_and_counter_continuity(self):
  self.assertEqual(w.parse_error(b'ER,T2,03\r')['protocol_error'],'03');self.assertEqual(w.counter_relation(32767,0,same_session=True)['classification'],'next');self.assertEqual(w.counter_relation(31,31,same_session=True)['classification'],'same');self.assertEqual(w.counter_relation(31,32)['classification'],'unknown')
if __name__=='__main__':unittest.main()
