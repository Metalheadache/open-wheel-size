"""Synthetic fixtures only: no real vehicle facts are embedded in tests."""
import copy,csv,hashlib,io,json,sys,tempfile,unittest,zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import validate as v
from release import build

class ValidationTests(unittest.TestCase):
 def setUp(self):
  self.s=v.load(v.ROOT/'schemas/catalog.schema.json')
  self.d={k:[] for k in v.TABLE_KEYS}
 def row(self,table,**updates):
  props=self.s['properties'][table]['items']['properties'];r={}
  for k,p in props.items():
   if 'enum' in p:r[k]=p['enum'][0]
   elif isinstance(p['type'],list):r[k]=None
   else:r[k]='fixture'
  r.update(updates);self.d[table].append(r);return r
 def fixture(self):
  self.row('platforms',platform_key='platform')
  scope=dict(model_year_start=2000,model_year_end=2000,reference_year=2000,configuration_reference='MY 2000 synthetic fixture',year_basis='manufacturerModelYear',market='ZZ')
  self.row('variants',variant_key='variant',platform_key='platform',**scope)
  self.row('sources',source_key='source',reference_url='https://example.org/synthetic',contribution_license='CC-BY-4.0')
  self.row('packages',package_key='package',variant_key='variant',source_key='source',**scope)
  for side in ['front','rear']:
   self.row('axles',package_key='package',axle=side,source_key='source',run_flat=None,xl_reinforced=None)
   for field,path in v.AXLE_PATHS.items():
    self.row('claims',claim_key=side+'-'+field,entity_type='oemWheelTyrePackage',entity_key='package',field_path=side+'.'+path,source_key='source',state='unknown',value=None,value_type='string',unknown_reason='notCollectedYet')
  for typ,key in [('source','source'),('vehiclePlatform','platform'),('vehicleVariant','variant'),('oemWheelTyrePackage','package')]:self.row('reviews',entity_type=typ,entity_key=key)
  return self.d
 def test_empty_valid(self):self.assertTrue(v.validate_data(self.d,self.s))
 def test_synthetic_unknowns_valid(self):self.assertTrue(v.validate_data(self.fixture(),self.s))
 def test_extra_private_field_rejected(self):
  self.fixture()['sources'][0]['private_notes']='not public'
  with self.assertRaisesRegex(ValueError,'unallowlisted'):v.validate_data(self.d,self.s)
 def test_duplicate_identity(self):
  self.fixture()['platforms'].append(copy.deepcopy(self.d['platforms'][0]))
  with self.assertRaisesRegex(ValueError,'Duplicate'):v.validate_data(self.d,self.s)
 def test_foreign_key(self):
  self.fixture()['variants'][0]['platform_key']='missing'
  with self.assertRaisesRegex(ValueError,'Missing platform'):v.validate_data(self.d,self.s)
 def test_missing_axle(self):
  self.fixture()['axles'].pop()
  with self.assertRaisesRegex(ValueError,'axle pair'):v.validate_data(self.d,self.s)
 def test_unknown_not_zero(self):
  self.fixture()['claims'][0]['value']=0
  with self.assertRaisesRegex(ValueError,'semantics'):v.validate_data(self.d,self.s)
 def test_numeric_not_string(self):
  self.fixture()['axles'][0]['wheel_width_in']='8'
  with self.assertRaisesRegex(ValueError,'wrong type'):v.validate_data(self.d,self.s)
 def test_mismatched_axle_claim(self):
  self.fixture()['axles'][0]['offset_mm']=0
  with self.assertRaisesRegex(ValueError,'disagreement'):v.validate_data(self.d,self.s)
 def test_years_not_inferred(self):
  self.fixture()['variants'][0]['model_year_end']=None
  with self.assertRaisesRegex(ValueError,'Half'):v.validate_data(self.d,self.s)
 def test_token_url(self):
  with self.assertRaisesRegex(ValueError,'Credential'):v.safe_url('https://example.org/?token=synthetic')
 def test_private_path(self):
  with self.assertRaisesRegex(ValueError,'private'):v.scan_text('/'+'Users/'+'example/private','fixture')
 def test_schema_cannot_be_relaxed(self):
  s=copy.deepcopy(self.s);s['additionalProperties']=True
  with self.assertRaises(ValueError):v.validate_data(self.d,s)
 def test_zero_completeness_is_na(self):self.assertIsNone(v.coverage(self.d)['field_completeness']['offset_mm']['percent'])
 def test_release_reproducible_and_checksums(self):
  with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
   x,h=build(v.ROOT,Path(a));y,j=build(v.ROOT,Path(b));self.assertEqual(x.read_bytes(),y.read_bytes());self.assertEqual(h,j)
   with zipfile.ZipFile(x) as z:
    prefix='open-wheel-size-'+v.load(v.ROOT/'manifest.json')['release_version']+'/'
    for line in z.read(prefix+'CHECKSUMS.sha256').decode().splitlines():
     digest,name=line.split('  ',1);self.assertEqual(hashlib.sha256(z.read(prefix+name)).hexdigest(),digest)
    for table in v.TABLE_KEYS:self.assertEqual(len(list(csv.DictReader(io.StringIO(z.read(prefix+'csv/'+table+'.csv').decode())))),0)
    with tempfile.TemporaryDirectory() as extracted:
     z.extractall(extracted);root=Path(extracted)/prefix
     self.assertEqual(v.validate_tree(root)['counts'],v.coverage(v.load(v.ROOT/'data/catalog.json'))['counts'])
     rebuilt,h2=build(root,Path(extracted)/'rebuilt');self.assertEqual(x.read_bytes(),rebuilt.read_bytes())
     (root/'csv/axles.csv').write_text('tampered\n')
     with self.assertRaisesRegex(ValueError,'checksum'):v.validate_tree(root)
if __name__=='__main__':unittest.main()
