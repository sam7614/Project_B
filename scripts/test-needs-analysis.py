import importlib.util,unittest,math
from pathlib import Path
spec=importlib.util.spec_from_file_location('needs',Path(__file__).with_name('analyze-needs.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def rows(items):
 return[dict(respondent_id=f'SYN-Q-{j+1:03}',role='developer-test',item_id=k,importance=str(a),current=str(b),synthetic='true')for k,pairs in items.items()for j,(a,b)in enumerate(pairs)]
class NeedsTests(unittest.TestCase):
 def test_published_worked_example(self):
  r=m.analyze(rows({'EXAMPLE':[(4,3),(5,4),(5,4),(3,4),(5,3)]}));self.assertAlmostEqual(r['items'][0]['borich_mwds'],3.52);self.assertTrue(r['items'][0]['lf_boundary'])
 def test_independent_arithmetic_and_axes(self):
  r=m.analyze(rows({'A':[(5,1),(5,2),(4,2),(4,3)],'B':[(3,2)]*4,'C':[(2,3)]*4}));a,b,c=r['items'];self.assertEqual(a['borich_mwds'],11.25);self.assertAlmostEqual(a['paired_t'],math.sqrt(15));self.assertEqual([i['lf_quadrant']for i in r['items']],['HH','LH','LL']);self.assertTrue(a['candidate_overlap']);self.assertFalse(b['candidate_overlap']);self.assertIsNone(b['paired_t']);self.assertIsNone(a['p_value'])
 def test_missing_pair_is_not_imputed(self):
  r=rows({'A':[(5,3),(4,2),(3,2)]});r[0]['current']='';s=m.analyze(r)['items'][0];self.assertEqual(s['n'],2);self.assertEqual(s['excluded_missing_pairs'],1)
 def test_duplicates_rejected(self):
  r=rows({'A':[(5,3),(4,2)]});self.assertRaises(ValueError,m.analyze,r+[r[0]])
 def test_mixed_roles_rejected(self):
  r=rows({'A':[(5,3),(4,2)]});r[0]['role']='faculty';self.assertRaises(ValueError,m.analyze,r)
 def test_impossible_non_synthetic_and_non_numeric_rejected(self):
  for patch in[{'importance':'NaN'},{'current':'6'},{'synthetic':'false'},{'importance':'1.5'},{'respondent_id':'actual-person'}]:
   r=rows({'A':[(5,3),(4,2)]});r[0].update(patch);self.assertRaises(ValueError,m.analyze,r)
 def test_equal_scores_keep_ties(self):
  r=m.analyze(rows({'A':[(4,2)]*3,'B':[(4,2)]*3}));self.assertEqual([i['borich_rank']for i in r['items']],[1,1]);self.assertTrue(all(i['lf_boundary']for i in r['items']));self.assertEqual(r['hh_count'],0)
if __name__=='__main__':unittest.main()
