"""Offline closed-schema and release checks, using only Python's standard library."""
import hashlib,json,math,re,sys
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl
ROOT=Path(__file__).resolve().parents[1]
TABLE_KEYS={'platforms':['platform_key'],'variants':['variant_key'],'packages':['package_key'],'axles':['package_key','axle'],'sources':['source_key'],'claims':['claim_key'],'reviews':['entity_type','entity_key']}
AXLE_PATHS={'wheel_diameter_in':'wheel.diameterInches','wheel_width_in':'wheel.widthInches','offset_mm':'wheel.offsetMillimetres','tyre_section_width_mm':'tyre.sectionWidthMillimetres','tyre_aspect_ratio_percent':'tyre.aspectRatioPercent','tyre_rim_diameter_in':'tyre.rimDiameterInches','actual_section_width_mm':'tyre.actualSectionWidthMillimetres','measuring_rim_width_in':'tyre.measuringRimWidthInches','spacer_mm':'spacerMillimetres','wheel_part_number':'wheel.partNumber','load_index':'tyre.loadIndex','speed_rating':'tyre.speedRating','tyre_brand':'tyre.brand','tyre_model':'tyre.model','run_flat':'tyre.runFlat','xl_reinforced':'tyre.xlReinforced'}
ENTITY_TABLE={'vehiclePlatform':'platforms','vehicleVariant':'variants','oemWheelTyrePackage':'packages','source':'sources','sourceRecord':'sources'}
def canonical(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False)+'\n'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def load(p):
 def pairs(items):
  d={}
  for k,v in items:
   require(k not in d,'Duplicate JSON property: '+k);d[k]=v
  return d
 return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))
def schema_check(v,s,path='$'):
 # Supports exactly the keywords used in our bundled closed schema.
 require(not set(s)-{'type','properties','required','additionalProperties','items','enum','$schema','title'},'Unsupported schema keyword')
 if 'enum' in s:require(any(type(v)==type(x) and v==x for x in s['enum']),path+': invalid enum')
 if 'type' in s:
  types=s['type'] if isinstance(s['type'],list) else [s['type']]
  actual='null' if v is None else 'boolean' if type(v)==bool else 'number' if type(v) in (int,float) else 'string' if type(v)==str else 'array' if type(v)==list else 'object' if type(v)==dict else 'invalid'
  require(actual in types,path+': wrong type')
  if actual=='number':require(math.isfinite(v),path+': nonfinite')
 if isinstance(v,dict):
  props=s['properties'];require(set(s['required'])<=set(v),path+': missing field')
  require(s['additionalProperties'] is False and not set(v)-set(props),path+': unallowlisted field')
  for k,x in v.items():schema_check(x,props[k],path+'.'+k)
 if isinstance(v,list):
  for i,x in enumerate(v):schema_check(x,s['items'],path+'['+str(i)+']')
def safe_url(value):
 u=urlsplit(value);require(u.scheme=='https' and bool(u.hostname) and not u.username and not u.password,'Unsafe citation URL')
 require(not any(re.search(r'(token|secret|password|signature|credential|api.?key|auth)',k,re.I) for k,v in parse_qsl(u.query)),'Credential-bearing citation URL')
def validate_data(d,s):
 schema_check(d,s);ix={}
 for table,keys in TABLE_KEYS.items():
  ix[table]={}
  for row in d[table]:
   key=tuple(row[k] for k in keys);require(all(type(k)==str and k.strip() for k in key),'Empty stable key')
   require(key not in ix[table],'Duplicate key: '+table);ix[table][key]=row
 for row in d['sources']:
  safe_url(row['reference_url'])
  require(all(row[k].strip() for k in ['source_key','title','publisher','attribution','public_release_basis']),'Missing source basis/attribution')
  require(row['contribution_license']=='CC-BY-4.0','Incompatible contribution licence; explicit notice/schema review required')
 def source(row):
  require((row['source_key'],) in ix['sources'],'Missing source');require(row['source_locator'].strip(),'Missing source locator')
 def dates(row):
  a,b,r=row['model_year_start'],row['model_year_end'],row['reference_year'];basis=row['year_basis']
  require((a is None)==(b is None),'Half model-year range')
  if a is not None:require(type(a)==int and type(b)==int and 1886<=a<=b<=2100,'Invalid model-year range')
  require(bool(row['configuration_reference']),'Missing dated/undated reference')
  if basis=='undatedConfiguration':require(a is None and r is None,'Undated year supplied')
  else:require(type(r)==int and 1886<=r<=2100,'Missing reference year')
  if basis=='manufacturerModelYear':require(a is not None and a<=r<=b,'Model-year basis lacks model years')
  if basis=='datedConfiguration':require(a is None,'Dated snapshot must not invent model years')
 for v in d['variants']:
  require((v['platform_key'],) in ix['platforms'],'Missing platform');dates(v)
 for p in d['packages']:
  require((p['variant_key'],) in ix['variants'],'Missing variant');source(p);dates(p)
  v=ix['variants'][(p['variant_key'],)]
  require(all(p[k]==v[k] for k in ['market','region','model_year_start','model_year_end','reference_year','configuration_reference','year_basis']),'Package applicability mismatch')
  require({r['axle'] for r in d['axles'] if r['package_key']==p['package_key']}=={'front','rear'},'Missing axle pair')
 claim_index={}
 for c in d['claims']:
  require(c['entity_type'] in ENTITY_TABLE,'Unknown entity type')
  require((c['entity_key'],) in ix[ENTITY_TABLE[c['entity_type']]],'Missing claim entity');source(c)
  if c['state']=='known':
   require(c['value'] is not None and c['unknown_reason'] is None,'Known claim semantics')
   require((type(c['value']) in (int,float) if c['value_type']=='number' else type(c['value'])==bool if c['value_type']=='boolean' else type(c['value'])==str),'Claim value type')
  else:require(c['value'] is None and bool(c['unknown_reason']),'Unknown/N/A semantics')
  claim_index.setdefault((c['entity_type'],c['entity_key'],c['field_path']),[]).append(c)
 for a in d['axles']:
  require((a['package_key'],) in ix['packages'],'Missing axle package');source(a)
  for f,path in AXLE_PATHS.items():
   value=a[f]
   if type(value) in (int,float):require(f=='offset_mm' or (value>=0 if f=='spacer_mm' else value>0),'Invalid dimension')
   claims=claim_index.get(('oemWheelTyrePackage',a['package_key'],a['axle']+'.'+path),[])
   require(bool(claims),'Axle field lacks provenance claim')
   require(any(type(c['value'])==type(value) and c['value']==value and (c['state']=='known')==(value is not None) for c in claims),'Axle/claim disagreement')
  w,t=a['wheel_diameter_in'],a['tyre_rim_diameter_in']
  if w is not None and t is not None:require(w==t,'Wheel/tyre rim mismatch')
 for r in d['reviews']:
  require(r['entity_type'] in ENTITY_TABLE and (r['entity_key'],) in ix[ENTITY_TABLE[r['entity_type']]],'Review entity missing')
  require(bool(r['public_release_basis'].strip()),'Missing release review basis')
 for kind,table in [('vehiclePlatform','platforms'),('vehicleVariant','variants'),('oemWheelTyrePackage','packages'),('source','sources')]:
  key=TABLE_KEYS[table][0]
  for row in d[table]:require((kind,row[key]) in ix['reviews'],'Missing public eligibility review')
 return True

def coverage(d):
 fields=['wheel_diameter_in','wheel_width_in','offset_mm','tyre_section_width_mm','tyre_aspect_ratio_percent','tyre_rim_diameter_in']
 years=[v[k] for v in d['variants'] for k in ['model_year_start','model_year_end'] if v[k] is not None]
 refs=[v['reference_year'] for v in d['variants'] if v['reference_year'] is not None]
 return {'counts':{k:len(v) for k,v in sorted(d.items())},'manufacturers':sorted({r['manufacturer'] for r in d['platforms']}),'manufacturer_count':len({r['manufacturer'] for r in d['platforms']}),'markets':sorted({r['market'] for r in d['variants'] if r['market']}),'model_year_range':[min(years),max(years)] if years else None,'reference_year_range':[min(refs),max(refs)] if refs else None,'technical_review_status':dict(Counter(r['technical_review_status'] for r in d['reviews'])),'claim_states':dict(Counter(r['state'] for r in d['claims'])),'conflicting_claims':sum(c['evidence_grade']=='conflicting' or c['unknown_reason']=='conflictingSources' for c in d['claims']),'field_completeness':{f:{'known':sum(a[f] is not None for a in d['axles']),'total':len(d['axles']),'percent':round(100*sum(a[f] is not None for a in d['axles'])/len(d['axles']),2) if d['axles'] else None} for f in fields}}
def coverage_md(c):
 rows='\n'.join('| '+k+' | '+str(v)+' |' for k,v in c['counts'].items())
 return '# Released coverage\n\nDATA RELEASE BLOCKED — zero vehicle records; tooling/docs only.\n\nGenerated from `data/catalog.json`; not a roadmap or private-master count.\n\n| Released table | Records |\n|---|---:|\n'+rows+'\n\nManufacturers: '+str(c['manufacturer_count'])+'. Markets: '+(', '.join(c['markets']) or 'none')+'.\nNo released model-year interval or technical reviews. Width, offset and tyre-size\ncompleteness are N/A (zero denominator), not 100%. No released conflicts does not\nmean the private master is conflict-free. See `coverage.json` for exact metrics.\n\nThe excluded private master retains 621 platform/generation rows, 6,349 variants,\n11,771 OEM packages, 23,542 axle rows, 2,390 sources and 732,391 claims. Those are\nnot public coverage. All are excluded pending a scoped fact-release basis.\nThe 157 research targets and historical 50-car sample are not current coverage.\n'
def scan_text(text,name):
 patterns=[r'-----BEGIN [A-Z ]*PRIVATE KEY-----',r'gh[pousr]_[A-Za-z0-9]{20,}',r'github_pat_[A-Za-z0-9_]{20,}',r'AKIA[A-Z0-9]{16}',r'postgres(?:ql)?://[^\s]+',r'(?i)(?:access_token|api_key|password)\s*[=:]\s*[\"\x27][A-Za-z0-9/+=_-]{12,}',r'/'+'Users/[^\s]+',r'/'+'home/[^\s]+']
 for pattern in patterns:require(not re.search(pattern,text),name+': private/secret pattern')
def validate_tree(root=ROOT):
 files=load(root/'PUBLIC_FILES.json');require(isinstance(files,list) and len(files)==len(set(files)),'Bad allowlist')
 actual=[]
 for p in root.rglob('*'):
  rel=p.relative_to(root)
  if any(x in {'.git','dist','__pycache__'} for x in rel.parts):continue
  require(not p.is_symlink(),'Symlink in public tree')
  if p.is_file():actual.append(rel.as_posix())
 require(set(actual)==set(files),'Public file allowlist mismatch')
 for f in files:
  require(not f.startswith('/') and '..' not in Path(f).parts,'Unsafe public path')
  scan_text((root/f).read_text(encoding='utf-8'),f)
 d=load(root/'data/catalog.json');s=load(root/'schemas/catalog.schema.json');validate_data(d,s)
 require((root/'data/catalog.json').read_text()==canonical(d),'Noncanonical JSON')
 c=coverage(d);require(load(root/'coverage.json')==c,'Stale coverage')
 require((root/'COVERAGE.md').read_text()==coverage_md(c),'Stale coverage documentation')
 require(load(root/'source-manifest.json')==d['sources'],'Stale source manifest')
 m=load(root/'manifest.json');require(m['released_counts']==c['counts'],'Manifest counts mismatch')
 require(m['catalog_sha256']==sha(root/'data/catalog.json'),'Data hash mismatch')
 require(m['schema_sha256']==sha(root/'schemas/catalog.schema.json'),'Schema hash mismatch')
 require(m['data_release_status']=='blocked' and not any(c['counts'].values()),'This tooling release cannot clear data eligibility')
 return c
if __name__=='__main__':
 try:
  c=validate_tree();print('PASS: offline structure, provenance, coverage, allowlist and content checks');print(json.dumps(c['counts'],sort_keys=True))
 except (ValueError,KeyError,TypeError) as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
