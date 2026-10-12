"""Deterministic allowlisted UTF-8 JSON/CSV release; offline, no publishing credentials."""
import argparse,csv,hashlib,io,json,zipfile
from pathlib import Path
from validate import ROOT,load,validate_tree

def build(root,output):
 validate_tree(root);output.mkdir(parents=True,exist_ok=True)
 version=load(root/'manifest.json')['release_version']
 members={n:(root/n).read_bytes() for n in load(root/'PUBLIC_FILES.json')}
 d=load(root/'data/catalog.json');s=load(root/'schemas/catalog.schema.json')
 for table,rows in d.items():
  fields=sorted(s['properties'][table]['items']['properties'])
  stream=io.StringIO(newline='');w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
  for row in rows:
   w.writerow({k:json.dumps(row[k],ensure_ascii=False,separators=(',',':'),allow_nan=False) for k in fields})
  members['csv/'+table+'.csv']=stream.getvalue().encode('utf-8')
 checks=''.join(hashlib.sha256(b).hexdigest()+'  '+n+'\n' for n,b in sorted(members.items()))
 members['CHECKSUMS.sha256']=checks.encode()
 archive=output/('open-wheel-size-'+version+'.zip')
 with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED) as z:
  for name,data in sorted(members.items()):
   info=zipfile.ZipInfo('open-wheel-size-'+version+'/'+name,(2026,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;z.writestr(info,data)
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()
 (output/'SHA256SUMS').write_text(digest+'  '+archive.name+'\n',encoding='utf-8')
 return archive,digest
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'dist');args=p.parse_args()
 archive,digest=build(ROOT,args.output);print(archive.name,digest)
