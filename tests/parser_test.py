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
 def test_sparse_html_no_guessed_data(self):self.assertEqual(m.parse_effects('<html><table></table></html>'),[])
if __name__=='__main__':unittest.main()
