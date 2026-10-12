"""Portable, deterministic UTF-8 JSON Lines utilities; standard library only."""
import gzip,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION='1.0.1'
def canonical(value):
 return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False)
def write_json(path,value):
 path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
def load(path):
 def pairs(items):
  d={}
  for k,v in items:
   if k in d:raise ValueError('Duplicate JSON property: '+k)
   d[k]=v
  return d
 return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs)
def rows(table,root=ROOT):
 index=load(root/'data/index.json')
 for item in index['tables'][table]['files']:
  with gzip.open(root/item['path'],'rt',encoding='utf-8') as f:
   for line in f:yield json.loads(line)
def write_rows(table,records,output,chunk_size=50000):
 files=[];count=0;stream=None;raw=None;part=0;part_count=0;uncompressed=None
 def close():
  stream.close();raw.close()
  files.append({'path':'data/'+path.name,'rows':part_count,'bytes':path.stat().st_size,'sha256':digest(path),'jsonl_sha256':uncompressed.hexdigest()})
 for row in records:
  if stream is None or part_count==chunk_size:
   if stream is not None:close()
   part+=1;part_count=0;path=output/(table+'-%03d.jsonl.gz'%part);raw=path.open('wb');stream=gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9);uncompressed=hashlib.sha256()
  b=(canonical(row)+'\n').encode('utf-8');stream.write(b);uncompressed.update(b);part_count+=1;count+=1
 if stream is not None:close()
 return {'rows':count,'files':files}
KEYS={'platforms':['platform_key'],'variants':['variant_key'],'packages':['package_key'],'axles':['package_key','axle'],'sources':['source_key'],'source_rights':['source_key'],'claims':['claim_key'],'reviews':['entity_type','entity_key'],'effective_facts':['fact_id'],'provenance':['record_id'],'corrections':['correction_id'],'known_issues':['issue_id']}
AXLE_PATHS={'wheel_diameter_in':'wheel.diameterInches','wheel_width_in':'wheel.widthInches','offset_mm':'wheel.offsetMillimetres','tyre_section_width_mm':'tyre.sectionWidthMillimetres','tyre_aspect_ratio_percent':'tyre.aspectRatioPercent','tyre_rim_diameter_in':'tyre.rimDiameterInches','actual_section_width_mm':'tyre.actualSectionWidthMillimetres','measuring_rim_width_in':'tyre.measuringRimWidthInches','spacer_mm':'spacerMillimetres','wheel_part_number':'wheel.partNumber','load_index':'tyre.loadIndex','speed_rating':'tyre.speedRating','tyre_brand':'tyre.brand','tyre_model':'tyre.model','run_flat':'tyre.runFlat','xl_reinforced':'tyre.xlReinforced'}
# These patterns detect accidental private material; an allowlist remains the primary boundary.
PRIVATE_PATTERNS=[r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'AKIA[A-Z0-9]{16}',r'postgres(?:ql)?://[^\s]+',r'/'+r'Users/[^\s]+',r'/'+r'home/(?!runner/)[^\s]+',r'(?i)\bBearer\s+[A-Za-z0-9._-]{15,}']
def scan(text):
 for p in PRIVATE_PATTERNS:
  if re.search(p,text):raise ValueError('Private content pattern detected')
