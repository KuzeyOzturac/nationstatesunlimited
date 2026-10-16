import unittest,importlib.util,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('importer',ROOT/'scripts/import-archive.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class ArchiveParser(unittest.TestCase):
 def test_real_issue_zero(self):
  options=m.parse_effects((ROOT/'data/fixtures/0.html').read_text());self.assertEqual([o['number'] for o in options],[1,2,3]);self.assertEqual(options[0]['text'],'voting is voluntary')
  r=next(r for r in options[0]['observations'] if r['stat']=='Political Freedom');self.assertEqual(r,{'stat':'Political Freedom','min':-12.56,'max':16.33,'mean':2.8011,'samples':4781})
  self.assertIn({'policy':'Autocracy','action':'add','conditional':True},options[2]['policyChanges'])
  self.assertIn({'policy':'Term Limits','action':'remove','conditional':False},options[2]['policyChanges'])
 def test_definite_autocracy(self):
  opts=m.parse_effects((ROOT/'data/fixtures/65.html').read_text());self.assertIn({'policy':'Autocracy','action':'add','conditional':False},opts[1]['policyChanges'])
 def test_shared_option_numbers_preserve_each_number(self):
  html='<html><table><tr><td>1/2. voting is voluntary</td><td><div>-1 to +3 Political Freedom (mean +2)</div></td><td><div>17</div><div>2026-10-16</div></td></tr></table></html>'
  opts=m.parse_effects(html);self.assertEqual([o['number'] for o in opts],[1,2]);self.assertEqual(opts[0]['observations'][0]['samples'],17);self.assertIsNot(opts[0]['observations'],opts[1]['observations'])
 def test_fixed_statistic_delta_is_not_dropped(self):
  html='<html><table><tr><td>1. an outcome</td><td><div>-2 Youth Rebelliousness</div></td><td><div>30</div></td></tr></table></html>'
  opts=m.parse_effects(html);self.assertEqual(opts[0]['observations'][0],{'stat':'Youth Rebelliousness','min':-2.0,'max':-2.0,'mean':-2.0,'samples':30,'fixed':True});self.assertEqual(opts[0]['notes'],[])
 def test_sparse_html_no_guessed_data(self):self.assertEqual(m.parse_effects('<html><table></table></html>'),[])
if __name__=='__main__':unittest.main()
