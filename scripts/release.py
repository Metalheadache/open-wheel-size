"""Build a portable archive from tagged public inputs, with lossless CSV tables."""
import argparse,csv,gzip,hashlib,io,json,tempfile,zipfile
from pathlib import Path
from common import ROOT,KEYS,load,digest,rows,canonical
from validate import validate_files,require

def build(root,output):
 validate_files(root);m=load(root/'manifest.json');index=load(root/'data/index.json')
 require(digest(root/'data/index.json')==m['data_index_sha256'],'Index hash mismatch')
 require(digest(root/'schemas/catalog.schema.json')==m['schema_sha256'],'Schema hash mismatch')
 for table,info in index['tables'].items():
  for f in info['files']:require(digest(root/f['path'])==f['sha256'],'Data hash mismatch')
 output.mkdir(parents=True,exist_ok=True);version=m['release_version'];prefix='open-wheel-size-'+version+'/'
 with tempfile.TemporaryDirectory() as directory:
  temp=Path(directory);members={n:root/n for n in load(root/'PUBLIC_FILES.json')}
  schema=load(root/'schemas/catalog.schema.json')['$defs']
  for table in KEYS:
   p=temp/(table+'.csv.gz');fields=sorted(schema[table]['properties'])
   with p.open('wb') as raw:
    with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0,compresslevel=9) as gz:
     with io.TextIOWrapper(gz,encoding='utf-8',newline='') as text:
      writer=csv.DictWriter(text,fieldnames=fields,lineterminator='\n');writer.writeheader()
      for row in rows(table,root):writer.writerow({k:canonical(row[k]) for k in fields})
   members['csv/'+p.name]=p
  checks=temp/'CHECKSUMS.sha256';checks.write_text(''.join(digest(p)+'  '+n+'\n' for n,p in sorted(members.items())),encoding='utf-8');members[checks.name]=checks
  archive=output/('open-wheel-size-'+version+'.zip')
  with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
   for name,p in sorted(members.items()):
    info=zipfile.ZipInfo(prefix+name,(2026,1,1,0,0,0));info.create_system=3;info.external_attr=0o100644<<16
    with z.open(info,'w',force_zip64=True) as dst,p.open('rb') as src:
     for chunk in iter(lambda:src.read(1048576),b''):dst.write(chunk)
  checksum=digest(archive);(output/'SHA256SUMS').write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
 return archive,checksum
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'dist');args=parser.parse_args();p,h=build(ROOT,args.output);print(p.name,h)
