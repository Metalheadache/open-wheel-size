"""Focused schema, confidentiality and deterministic-format regression tests."""
import copy,gzip,json,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import canonical,load,ROOT,write_rows,scan
from project import schema,clean,select,FIELDS
from validate import schema_check,safe_url,interval
class CatalogTests(unittest.TestCase):
 def test_schema_closed(self):
  s=schema()['$defs']['platforms'];r={k:None for k in s['properties']};r['private_notes']='excluded'
  with self.assertRaisesRegex(ValueError,'unexpected'):schema_check(r,s)
 def test_dimension_numeric(self):
  s=schema()['$defs']['axles'];r={k:None for k in s['properties']};r['wheel_width_in']='8'
  with self.assertRaisesRegex(ValueError,'wrong type'):schema_check(r,s)
 def test_boolean_not_dimension(self):
  with self.assertRaises(ValueError):schema_check(True,{'type':['number','null']})
 def test_unknown_null(self):self.assertIsNone(clean(''))
 def test_zero_preserved(self):self.assertEqual(clean(0),0)
 def test_rights_not_promoted(self):
  p={'source_key':'synthetic','licence_status':'notPermitted','redistribution_permission':'unknown'}
  r=select(p,FIELDS['source_rights']);self.assertEqual(r['licence_status'],'notPermitted');self.assertEqual(r['redistribution_permission'],'unknown')
 def test_private_fields_excluded(self):
  r=select({'source_key':'x','rights_reviewer':'private'},FIELDS['sources']);self.assertNotIn('rights_reviewer',r)
 def test_private_locator_redacted(self):
  value=clean('/'+'Users/'+'example/a.pdf; page 12');self.assertIn('page 12',value);self.assertNotIn('example',value)
 def test_url_secrets_stripped(self):
  self.assertEqual(clean('https://example.org/spec?model=1&token=secret','reference_url'),'https://example.org/spec?model=1')
 def test_url_scanner(self):
  with self.assertRaisesRegex(ValueError,'Tokenized'):safe_url('https://example.org?password=synthetic')
 def test_scanner(self):
  with self.assertRaises(ValueError):scan('/'+'Users/'+'example/private')
 def test_half_year_rejected(self):
  with self.assertRaises(ValueError):interval({'model_year_start':2000,'model_year_end':None})
 def test_undated_scope(self):
  with self.assertRaises(ValueError):interval({'year_basis':'undatedConfiguration','model_year_start':2000,'model_year_end':2000})
 def test_deterministic_shards(self):
  records=[{'id':i,'value':None} for i in range(5)]
  with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
   x=write_rows('synthetic',iter(records),Path(a),2);y=write_rows('synthetic',iter(records),Path(b),2);self.assertEqual(x,y)
   recovered=[]
   for item in x['files']:
    pa=Path(a)/Path(item['path']).name;pb=Path(b)/pa.name;self.assertEqual(pa.read_bytes(),pb.read_bytes())
    with gzip.open(pa,'rt',encoding='utf-8') as f:recovered.extend(json.loads(line) for line in f)
   self.assertEqual(records,recovered)
 def test_nan_rejected(self):
  with self.assertRaises(ValueError):canonical(float('nan'))
if __name__=='__main__':unittest.main()
