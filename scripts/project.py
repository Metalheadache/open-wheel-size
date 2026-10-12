"""Allowlisted projection of an existing reconciled SQLite ledger. Never edits it.

Run privately with --ledger and --output. No credentials, network or database
connection is required. Rights labels are preserved, never promoted to permitted.
"""
import argparse,collections,json,re,sqlite3,uuid
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit,parse_qsl,urlencode
from common import canonical,write_json,write_rows,scan,KEYS

FIELDS={
'sources': 'source_key title publisher issuing_organization source_type source_version publication_date retrieval_date reference_url language market jurisdiction content_hash attribution_requirement'.split(),
'source_rights':'source_key licence_status commercial_use_permission redistribution_permission rights_scope rights_reference_url rights_source_locator rights_checked_at attribution_requirement permitted_use_description'.split(),
'platforms':'platform_key manufacturer model_family chassis_generation aliases_en aliases_zh'.split(),
'variants':'variant_key platform_key aliases_en aliases_zh body_style brake_package_display_name brake_package_key configuration_reference drive_type engine_code engine_description engine_family factory_brake_package factory_suspension_package market model_year_end model_year_start package_code production_end production_start reference_year region suspension_package_display_name suspension_package_key transmission_name transmission_type trim year_basis'.split(),
'packages':'package_key variant_key package_name package_type option_package_code wheel_style_code brake_package_applicability brake_package_key configuration_reference market model_year_end model_year_start reference_year region source_key source_locator suspension_package_applicability suspension_package_key transmission_applicability year_basis'.split(),
'axles':'package_key axle actual_section_width_mm evidence_grade load_index measuring_rim_width_in offset_mm run_flat source_key source_locator spacer_mm speed_rating tyre_aspect_ratio_percent tyre_brand tyre_model tyre_rim_diameter_in tyre_section_width_mm wheel_diameter_in wheel_part_number wheel_width_in xl_reinforced'.split(),
'claims':'claim_key axle brake_package canonical_unit drivetrain entity_key entity_type evidence_grade field_path market model_year_end model_year_start original_unit package_code region source_key source_locator state suspension_package trim unknown_reason value value_type'.split(),
'reviews':'entity_type entity_key blocking_issue_count publication_status research_status rights_review_status technical_review_status'.split(),
'effective_facts':'fact_id axle entity_key field table value canonical_unit review_status source_locator capture_sha256 source_id batch_id gap_id evidence_group'.split(),
'provenance':'entity_key variant_key axle field table value unit status review_status applicability_state fact_id event_id cell_id hardware_cell_id inventory_id source_id source_key source_locator capture_sha256 canonical_record_sha256 original_field_path field_dictionary_version previous_state next_state dependency_fact_id dependency_fact_ids dependency_claim_id unallocated_existing_claim_id'.split(),
'corrections':'correction_id axle entity_key field old_value value proposed_value impacted_fact_ids application_status accepted_at source_locator source_sha256 evidence_ref'.split(),
'known_issues':'issue_id subject status finding limitation source_reference affected_keys'.split()}
APPLICABILITY='market region model_year model_year_start model_year_end reference_year year_basis configuration_reference body body_style drive_type transmission_name transmission_type trim option_package_code package_type package_key variant_key wheel_style_code suspension_configuration suspension_requirement suspension_scope body_configuration own_axle_clause factory_set_scope selected_catalog_market selected_catalog_model selected_catalog_production selected_catalog_type_code manufacturer_model_year actual_manufacturer_model_year no_part_code_or_finish_assignment factory_finish_not_assigned part_linkage_only catalogue_part_linkage_only production_month_not_assigned reference_year_preserved'.split()
SUPPORT='source_id source_key source_locator locator role capture_sha256'.split()
KINDS={'sources':'source','platforms':'platform','variants':'variant','packages':'package','axles':'axle','claims':'claim','reviews':'review','effective_facts':'effective_fact','provenance':'provenance','corrections':'correction'}
TEXT_NULL={'type':['string','null']};SCALAR={'type':['string','number','boolean','null']}
def schema():
 tables={}
 for table,fields in FIELDS.items():
  props={f:SCALAR for f in fields};props['record_id']=TEXT_NULL;props['stable_id']=TEXT_NULL
  if table in ['effective_facts','provenance']:
   props['applicability']={'type':'object','properties':{f:SCALAR for f in APPLICABILITY},'additionalProperties':False}
   props['supporting_evidence']={'type':'array','items':{'type':'object','properties':{f:SCALAR for f in SUPPORT},'additionalProperties':False}}
   props['qualifications']={'type':'array','items':{'type':'string'}}
  if table=='effective_facts':
   props.update({f:TEXT_NULL for f in ['source_key','claim_stable_id','axle_stable_id']})
  if table=='provenance':props['provenance_key']=SCALAR
  for f in ['wheel_diameter_in','wheel_width_in','offset_mm','tyre_section_width_mm','tyre_aspect_ratio_percent','tyre_rim_diameter_in','actual_section_width_mm','measuring_rim_width_in','spacer_mm','model_year_start','model_year_end','reference_year','blocking_issue_count']:
   if f in props and (f not in ['model_year_start','model_year_end','reference_year'] or table in ['variants','packages']):props[f]={'type':['number','null']}
  for f in ['dependency_fact_ids','impacted_fact_ids','affected_keys']:
   if f in props:props[f]={'type':['array','null'],'items':{'type':'string'}}
  tables[table]={'type':'object','properties':props,'required':list(props),'additionalProperties':False}
 return {'$schema':'https://json-schema.org/draft/2020-12/schema','title':'open-wheel-size portable row schemas 2.0','$defs':tables}
def text_clean(s):
 # Remove internal locators, not publisher names, public citations or technical dimensions.
 s=re.sub(r'(?:/'+r'Users/|/'+r'home/)[^\s;,\]\)\"\x27]+','[private path omitted]',s)
 s=re.sub(r'(?<!https://)(?:research|outputs|integration/private)/[^\s;,\]\)\"\x27]+','[private reference omitted]',s)
 s=re.sub(r'(?i)wheel'+'osophy','upstream catalog',s)
 return s

def clean(value,field=''):
 if value=='' or value is None:return None
 if isinstance(value,dict) and 'excel_date' in value:return value['excel_date']
 if isinstance(value,str):
  value=text_clean(value)
  if field.endswith('_url') or field=='reference_url':
   u=urlsplit(value)
   if u.scheme not in ('http','https') or not u.hostname:raise ValueError('Nonpublic citation URL')
   query=[(k,v) for k,v in parse_qsl(u.query,keep_blank_values=True) if not re.search(r'(?i)(token|password|secret|signature|credential|api.?key|auth)',k)]
   value=urlunsplit((u.scheme,u.hostname+(':'+str(u.port) if u.port else ''),u.path,urlencode(query),u.fragment))
  scan(value)
 return value

def select(p,fields):return {f:clean(p.get(f),f) for f in fields}
def qualifications(p):
 text=canonical(p).lower();out=[]
 for label,terms in {'authoredExtract':['authored extract','webtoolresearchextract','researcher-authored'],'independentCatalog':['independent catalog','independent reproduction'],'scopeInterpretation':['scope interpretation','scopedinterpretation'],'branchInvariance':['invariant','invariance'],'sameAssemblyNormalization':['same-assembly','same assembly'],'sourceConflict':['conflict','disagree'],'retrospectiveSource':['retrospect']}.items():
  if any(t in text for t in terms):out.append(label)
 return sorted(out)

def project(ledger,output,private_report):
 output.mkdir(parents=True,exist_ok=True);data=output/'data';data.mkdir(exist_ok=True)
 c=sqlite3.connect(ledger.resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
 batch=c.execute('select batch_id from batches').fetchall();assert len(batch)==1
 exclusions=collections.Counter();redactions=collections.Counter();identities={};sources={}
 facts={};factlinks={r[0]:r[1:] for r in c.execute('select fact_id,axle_row_id,claim_id from fact_links')}
 for s, in c.execute("select payload from rows where kind='provenance'"):
  p=json.loads(s)
  if isinstance(p['value'],dict) and 'fact' in p['value']:facts[p['key']]=p['value']
 def records(table):
  kind=KINDS.get(table,'source' if table=='source_rights' else 'release_history')
  for rid,sid,key,payload in c.execute('select record_id,proposed_db_id,stable_key,payload from rows where kind=? order by stable_key,record_id',(kind,)):
   p=json.loads(payload)
   if table=='known_issues':
    if not str(p.get('0')).startswith('S3P-'):continue
    p=dict(zip(FIELDS[table],[p.get(str(i)) for i in range(7)]));p['affected_keys']=(p.get('affected_keys') or '').splitlines()
   original=p
   if table=='provenance':
    inner=p['value'];p=inner.get('fact',inner)
    if not isinstance(p,dict):p={}
   row=select(p,FIELDS[table]);row.update(record_id=rid,stable_id=sid)
   if table=='provenance':row['provenance_key']=original['key'] if '/' not in str(original['key']) else None
   if table in ['effective_facts','provenance']:
    app=p.get('applicability');row['applicability']=select(app,APPLICABILITY) if isinstance(app,dict) else select({},APPLICABILITY)
    support=p.get('supporting_evidence') or [];row['supporting_evidence']=[select(x,SUPPORT) for x in support if isinstance(x,dict)]
    row['qualifications']=qualifications(original)
   if table=='effective_facts':
    row['source_key']=facts[p['fact_id']]['source_key'];row['axle_stable_id'],row['claim_stable_id']=factlinks[p['fact_id']]
   if table=='provenance' and 'fact' in original['value']:row['source_key']=original['value'].get('source_key')
   for k in set(p)-set(FIELDS[table]):exclusions[table+'.'+k]+=1
   for k,v in row.items():
    if isinstance(v,str) and ('[private ' in v or v!=p.get(k) and k.endswith('_url')):redactions[table+'.'+k]+=1
   if table=='sources':sources[row['source_key']]=row
   scan(canonical(row));yield row
 index={'schema_version':'2.0','source_batch_id':batch[0][0],'tables':{}}
 for table in FIELDS:
  index['tables'][table]=write_rows(table,records(table),data)
  print(table,index['tables'][table]['rows'],flush=True)
 write_json(data/'index.json',index)
 (output/'schemas').mkdir(exist_ok=True);write_json(output/'schemas/catalog.schema.json',schema())
 report={'source_batch_id':batch[0][0],'published_counts':{k:v['rows'] for k,v in index['tables'].items()},'excluded_field_occurrences':dict(exclusions),'sanitized_field_occurrences':dict(redactions),'excluded_nondata_kinds':dict(c.execute("select kind,count(*) from rows where kind not in ('source','platform','variant','package','axle','claim','review','effective_fact','provenance','correction') group by kind")),'rights_gate':'owner explicitly superseded for structured facts; labels preserved; no legal clearance asserted'}
 if private_report:write_json(private_report,report)
 return index
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--ledger',type=Path,required=True);parser.add_argument('--output',type=Path,required=True);parser.add_argument('--private-report',type=Path);args=parser.parse_args()
 project(args.ledger,args.output,args.private_report)
