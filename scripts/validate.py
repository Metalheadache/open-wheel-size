"""Offline streaming validation of the complete sanitized projection."""
import collections,gzip,hashlib,json,math,re,sqlite3,sys,tempfile
from pathlib import Path
from urllib.parse import urlsplit,parse_qsl
from common import ROOT,KEYS,AXLE_PATHS,canonical,load,digest,rows,scan,write_json

def require(ok,message):
 if not ok:raise ValueError(message)
def schema_check(v,s,path='$'):
 if 'enum' in s:require(v in s['enum'],path+': enum')
 if 'type' in s:
  types=s['type'] if isinstance(s['type'],list) else [s['type']]
  actual='null' if v is None else 'boolean' if type(v)==bool else 'number' if type(v) in (int,float) else 'string' if type(v)==str else 'array' if type(v)==list else 'object' if type(v)==dict else 'invalid'
  require(actual in types,path+': wrong type')
  if actual=='number':require(math.isfinite(v),path+': nonfinite')
 if isinstance(v,dict):
  require(s.get('additionalProperties') is False,path+': schema must be closed')
  require(not set(v)-set(s['properties']),path+': unexpected field')
  require(set(s.get('required',[]))<=set(v),path+': missing field')
  for k,x in v.items():schema_check(x,s['properties'][k],path+'.'+k)
 if isinstance(v,list):
  for i,x in enumerate(v):schema_check(x,s['items'],path+'[]')
def safe_url(value):
 if value is None:return
 u=urlsplit(value);require(u.scheme in ('http','https') and bool(u.hostname) and not u.username and not u.password,'Unsafe source URL')
 require(not any(re.search(r'(?i)(token|secret|password|credential|signature|api.?key|auth)',k) for k,v in parse_qsl(u.query)),'Tokenized URL')
def interval(row):
 a,b=row.get('model_year_start'),row.get('model_year_end');require((a is None)==(b is None),'Half year interval')
 if a is not None:require(type(a) in (int,float) and type(b) in (int,float) and a==int(a) and b==int(b) and 1886<=a<=b<=2100,'Invalid model-year interval')
 r=row.get('reference_year')
 if r is not None:require(type(r) in (int,float) and 1886<=r<=2100 and r==int(r),'Invalid reference year')
 # Legacy rows may have no v1.2 reference fields; do not fabricate them.
 if row.get('year_basis')=='undatedConfiguration':require(a is None and r is None,'Undated row has year')
def validate(root=ROOT,check_generated=True):
 index=load(root/'data/index.json');schema=load(root/'schemas/catalog.schema.json')['$defs']
 require(set(index['tables'])==set(KEYS)==set(schema),'Table/schema mismatch')
 with tempfile.TemporaryDirectory() as temp:
  c=sqlite3.connect(str(Path(temp)/'check.sqlite'))
  c.executescript('PRAGMA journal_mode=OFF; PRAGMA synchronous=OFF; CREATE TABLE ids(t TEXT,k TEXT,rid TEXT,sid TEXT,PRIMARY KEY(t,k)); CREATE INDEX rid ON ids(t,rid); CREATE INDEX sid ON ids(t,sid); CREATE TABLE refs(t TEXT,k TEXT,context TEXT); CREATE TABLE claims(entity TEXT,field TEXT,state TEXT,value TEXT); CREATE INDEX cf ON claims(entity,field);')
  small={};counts={};states=collections.Counter();grades=collections.Counter();warnings=collections.Counter()
  for table,info in index['tables'].items():
   count=0;small[table]=[]
   for item in info['files']:
    name=item['path'];require(name.startswith('data/') and '..' not in Path(name).parts,'Unsafe data path');p=root/name
    require(p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],'File hash mismatch: '+name)
    uncompressed=hashlib.sha256();part=0
    with gzip.open(p,'rb') as stream:
     for line in stream:
      uncompressed.update(line);r=json.loads(line);require((canonical(r)+'\n').encode()==line,'Noncanonical JSONL');schema_check(r,schema[table]);scan(line.decode());part+=1;count+=1
      key=canonical([r[k] for k in KEYS[table]]);require(all(r[k] is not None for k in KEYS[table]),'Null identity')
      try:c.execute('insert into ids values (?,?,?,?)',(table,key,r['record_id'],r['stable_id']))
      except sqlite3.IntegrityError:raise ValueError('Duplicate identity in '+table)
      def ref(t,key,context):
       if key is not None:c.execute('insert into refs values (?,?,?)',(t,canonical([key]),context))
      if table not in ('claims','provenance'):small[table].append(r)
      if table=='sources':safe_url(r['reference_url']);require(r['reference_url'] and r['source_key'],'Missing source citation')
      if table=='source_rights':ref('sources',r['source_key'],'rights');safe_url(r['rights_reference_url'])
      if table=='variants':ref('platforms',r['platform_key'],'variant');interval(r)
      if table=='packages':ref('variants',r['variant_key'],'package');ref('sources',r['source_key'],'package source');interval(r)
      if table=='axles':
       ref('packages',r['package_key'],'axle');ref('sources',r['source_key'],'axle source');require(r['axle'] in ('front','rear'),'Axle enum')
       for f in ['wheel_diameter_in','wheel_width_in','offset_mm','tyre_section_width_mm','tyre_aspect_ratio_percent','tyre_rim_diameter_in','actual_section_width_mm','measuring_rim_width_in','spacer_mm']:
        val=r[f];require(val is None or type(val) in (int,float),'Dimension must be numeric')
        if val is not None:require(f=='offset_mm' or (val>=0 if f=='spacer_mm' else val>0),'Invalid dimension')
       if r['wheel_diameter_in'] is not None and r['tyre_rim_diameter_in'] is not None:require(r['wheel_diameter_in']==r['tyre_rim_diameter_in'],'Wheel/tyre rim inconsistency')
      if table in ('claims','reviews'):
       target={'vehicleVariant':'variants','oemWheelTyrePackage':'packages','vehiclePlatform':'platforms','source':'sources','sourceRecord':'sources'}.get(r['entity_type']);require(target is not None,'Unsupported entity type');ref(target,r['entity_key'],'entity')
      if table=='claims':
       ref('sources',r['source_key'],'claim source');require(r['source_key'] and r['source_locator'],'Claim lacks source/locator')
       state=r['state'];states[state]+=1;grades[r['evidence_grade']]+=1;require(state in ('known','unknown','notApplicable'),'State enum')
       if state=='known':
        require(r['value'] is not None,'Known null');vt=r['value_type']
        require((type(r['value']) in (int,float) if vt=='number' else type(r['value'])==bool if vt=='boolean' else type(r['value'])==str if vt=='string' else False),'Claim type')
       else:require(r['value'] is None,'Unknown/N/A has value')
       c.execute('insert into claims values (?,?,?,?)',(r['entity_key'],r['field_path'],state,canonical(r['value'])))
      if table=='effective_facts':ref('packages',r['entity_key'],'fact');ref('sources',r['source_key'],'fact source')
    require(part==item['rows'] and uncompressed.hexdigest()==item['jsonl_sha256'],'JSONL count/hash mismatch')
   require(count==info['rows'],'Table count mismatch');counts[table]=count;c.commit()
  broken=c.execute('select context,count(*) from refs left join ids using(t,k) where ids.k is null group by context').fetchall();require(not broken,'Broken relationships: '+str(broken))
  require(counts['sources']==counts['source_rights'],'Rights row coverage')
  pairs=collections.Counter(r['package_key'] for r in small['axles']);require(all(pairs[r['package_key']]==2 for r in small['packages']),'Two axles per package required')
  for f in small['effective_facts']:
   require(c.execute("select 1 from ids where t='claims' and sid=?",(f['claim_stable_id'],)).fetchone(),'Fact claim link missing')
   require(c.execute("select 1 from ids where t='axles' and sid=?",(f['axle_stable_id'],)).fetchone(),'Fact axle link missing')
  # Reconcile current axle fields against all historical claims; do not erase older unknowns.
  discrepancies=[]
  for a in small['axles']:
   for field,path in AXLE_PATHS.items():
    val=a[field];val={'yes':True,'no':False,'unknown':None}.get(val,val) if field in ('run_flat','xl_reinforced') else val
    cs=c.execute('select state,value from claims where entity=? and field=?',(a['package_key'],a['axle']+'.'+path)).fetchall()
    def comparable(value):
     if field in ('run_flat','xl_reinforced') and isinstance(value,str):return {'yes':True,'no':False,'unknown':None}.get(value.lower(),value)
     if field=='load_index' and value is not None:return str(value)
     return value
    if not any(comparable(json.loads(cv))==comparable(val) and (state=='known')==(val is not None) for state,cv in cs):
     discrepancies.append({'package_key':a['package_key'],'axle':a['axle'],'field':field,'canonical_value':a[field],'claims':[{'state':state,'value':json.loads(cv)} for state,cv in cs],'disposition':'preserved_unresolved_no_publication_correction'})
  coverage=make_coverage(small,counts,states,grades)
  coverage['reconciliation']={'axle_claim_discrepancies':discrepancies,'missing_axle_claim_links':sum(not d['claims'] for d in discrepancies),'conflicting_axle_claim_values':sum(bool(d['claims']) for d in discrepancies),'broken_foreign_keys':0,'source_master_values_preserved':True}
 if check_generated:
  require(load(root/'coverage.json')==coverage,'Stale coverage')
  require(load(root/'reconciliation.json')==coverage['reconciliation'],'Stale reconciliation')
  m=load(root/'manifest.json');require(m['released_counts']==counts,'Manifest count mismatch');require(m['data_index_sha256']==digest(root/'data/index.json'),'Index mismatch');require(m['schema_sha256']==digest(root/'schemas/catalog.schema.json'),'Schema hash mismatch')
  require(m['rights_clearance']=='notAsserted','Rights clearance must not be implied')
  require((root/'COVERAGE.md').read_text()==coverage_md(coverage),'Stale coverage markdown')
  require(load(root/'source-manifest.json')=={'sources':index['tables']['sources'],'source_rights':index['tables']['source_rights']},'Source manifest mismatch')
 return coverage

def make_coverage(small,counts,states,grades):
 ax=small['axles'];variants=small['variants'];years=[v[k] for v in variants for k in ['model_year_start','model_year_end'] if v[k] is not None];refs=[v['reference_year'] for v in variants if v['reference_year'] is not None]
 return {'counts':counts,'manufacturer_count':len({r['manufacturer'] for r in small['platforms']}),'manufacturers':sorted({r['manufacturer'] for r in small['platforms']}),'markets':dict(sorted(collections.Counter(v['market'] for v in variants).items())),'model_year_range':[min(years),max(years)] if years else None,'reference_year_range':[min(refs),max(refs)] if refs else None,'technical_review_status':dict(collections.Counter(r['technical_review_status'] for r in small['reviews'])),'rights_review_status':dict(collections.Counter(r['rights_review_status'] for r in small['reviews'])),'source_licence_status':dict(collections.Counter(r['licence_status'] for r in small['source_rights'])),'source_redistribution_permission':dict(collections.Counter(r['redistribution_permission'] for r in small['source_rights'])),'claim_states':dict(states),'claim_evidence_grades':dict(grades),'known_issue_status':dict(collections.Counter(r['status'] for r in small['known_issues'])),'field_completeness':{f:{'known':sum(a[f] is not None for a in ax),'unknown':sum(a[f] is None for a in ax),'total':len(ax),'percent':round(100*sum(a[f] is not None for a in ax)/len(ax),2)} for f in ['wheel_diameter_in','wheel_width_in','offset_mm','tyre_section_width_mm','tyre_aspect_ratio_percent','tyre_rim_diameter_in']}}
def coverage_md(c):
 lines=['# Released coverage','','Complete sanitized structured v1 scope; unresolved rights labels preserved.','Owner-authorized publication is not legal clearance or technical approval.','','| Table | Records |','|---|---:|']
 lines += ['| '+k+' | '+str(v)+' |' for k,v in sorted(c['counts'].items())]
 lines += ['', 'Manufacturer labels: '+str(c['manufacturer_count'])+' (original aliases/capitalization retained; not a normalized corporate count). Platform counts are platform/generation','keys; variant counts represent scoped market/year/trim configurations, not platforms.','','Explicit model years: '+str(c['model_year_range'])+'. Dated reference years: '+str(c['reference_year_range'])+'.','Reference dates do not automatically imply manufacturer model years.','','| Axle field | Known | Unknown | Completeness |','|---|---:|---:|---:|']
 lines += ['| '+k+' | '+str(v['known'])+' | '+str(v['unknown'])+' | '+str(v['percent'])+'% |' for k,v in sorted(c['field_completeness'].items())]
 lines += ['', 'Market scopes (GLOBAL, ACEA, EU and unknown are not country assignments):','', ', '.join(k+': '+str(v) for k,v in sorted(c['markets'].items())),'', 'Technical reviews: '+json.dumps(c['technical_review_status'],sort_keys=True)+'.','Source redistribution labels: '+json.dumps(c['source_redistribution_permission'],sort_keys=True)+'.','Claim states: '+json.dumps(c['claim_states'],sort_keys=True)+'.','','Canonical axle/claim discrepancies: '+str(len(c['reconciliation']['axle_claim_discrepancies']))+'. See `reconciliation.json`.','See `known_issues` for scoped unresolved conflicts and qualifications. Historical','unknown claims can coexist with later known claims; use the canonical axle table','for current wheel values and retain the full claim history for provenance.','Chinese aliases do not establish China applicability; OEM geometry is not','aftermarket fitment; nominal tyre width is not actual measured width.','The historical 50-car sample and 157 research targets are not released coverage.','']
 return '\n'.join(lines)

def validate_files(root=ROOT):
 allowed=load(root/'PUBLIC_FILES.json');actual=[]
 for p in root.rglob('*'):
  rel=p.relative_to(root)
  if any(x in {'.git','dist','__pycache__'} for x in rel.parts):continue
  require(not p.is_symlink(),'Symlink in public tree')
  if p.is_file():actual.append(rel.as_posix())
 generated={'CHECKSUMS.sha256'}|{'csv/'+t+'.csv.gz' for t in KEYS}
 extras=set(actual)-set(allowed);require(extras in (set(),{'CHECKSUMS.sha256'},generated) and set(allowed)<=set(actual),'Public file allowlist mismatch')
 if extras:
  checks={}
  for line in (root/'CHECKSUMS.sha256').read_text().splitlines():
   h,n=line.split('  ',1);require(n not in checks,'Duplicate checksum');checks[n]=h
  require(set(checks)==set(allowed)| (extras-{'CHECKSUMS.sha256'}),'Checksum allowlist mismatch')
  for n,h in checks.items():require(digest(root/n)==h,'Archive checksum mismatch')
 for name in allowed:
  require(not Path(name).is_absolute() and '..' not in Path(name).parts,'Unsafe file path')
  if not name.endswith('.gz'):scan((root/name).read_text())
 return True
if __name__=='__main__':
 try:validate_files();c=validate();print('PASS: complete offline validation');print(json.dumps(c['counts'],sort_keys=True))
 except (ValueError,KeyError,TypeError,sqlite3.Error) as e:print('FAIL:',e,file=sys.stderr);sys.exit(1)
