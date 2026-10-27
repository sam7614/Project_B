import importlib.util,unittest,copy,csv
from pathlib import Path
from reportlab.graphics import renderSVG
ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('lf',Path(__file__).with_name('render-lf-fixture.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
spec2=importlib.util.spec_from_file_location('needs',Path(__file__).with_name('analyze-needs.py'));a=importlib.util.module_from_spec(spec2);spec2.loader.exec_module(a)
class PlotTests(unittest.TestCase):
 def setUp(self):self.s=a.analyze(list(csv.DictReader((ROOT/'research/data/needs-fixture.csv').read_text(encoding='utf-8-sig').splitlines())))
 def test_labels_and_coordinates(self):
  svg=renderSVG.drawToString(m.drawing_for(self.s));self.assertIn('DEVELOPMENT ONLY',svg);self.assertIn('real respondents: 0',svg);self.assertIn('A (4.50, 2.50)',svg);self.assertIn('3.166667',svg);self.assertIn('0.833333',svg)
 def test_real_or_unlabelled_rejected(self):
  for patch in[{'real_participants':4},{'purpose':'survey'}]:s=copy.deepcopy(self.s);s.update(patch);self.assertRaises(ValueError,m.drawing_for,s)
 def test_non_finite_and_out_of_range_rejected(self):
  for bad in[float('nan'),6]:s=copy.deepcopy(self.s);s['items'][0]['mean_importance']=bad;self.assertRaises(ValueError,m.drawing_for,s)
if __name__=='__main__':unittest.main()
