"""Build a portable archive from tagged public inputs, without recompressing tagged inputs."""
import argparse,struct,tempfile,zlib
from pathlib import Path
from common import ROOT,load,digest
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
  checks=temp/'CHECKSUMS.sha256';checks.write_text(''.join(digest(p)+'  '+n+'\n' for n,p in sorted(members.items())),encoding='utf-8');members[checks.name]=checks
  archive=output/('open-wheel-size-'+version+'.zip')
  # Explicit ZIP32 stored headers avoid Python-version-specific ZIP64 metadata.
  # Public archives are far below the ZIP32 file/count/offset limits.
  central=[];date=(2026-1980)<<9 | 1<<5 | 1
  with archive.open('wb') as z:
   for name,p in sorted(members.items()):
    filename=(prefix+name).encode('utf-8');size=p.stat().st_size;crc=0
    require(size<0xffffffff and z.tell()<0xffffffff,'ZIP32 size limit exceeded')
    with p.open('rb') as src:
     for chunk in iter(lambda:src.read(1048576),b''):crc=zlib.crc32(chunk,crc)
    offset=z.tell();crc &= 0xffffffff
    z.write(struct.pack('<IHHHHHIIIHH',0x04034b50,20,0x800,0,0,date,crc,size,size,len(filename),0));z.write(filename)
    with p.open('rb') as src:
     for chunk in iter(lambda:src.read(1048576),b''):z.write(chunk)
    central.append(struct.pack('<IHHHHHHIIIHHHHHII',0x02014b50,(3<<8)|20,20,0x800,0,0,date,crc,size,size,len(filename),0,0,0,0,0o100644<<16,offset)+filename)
   start=z.tell()
   for entry in central:z.write(entry)
   length=z.tell()-start;require(len(central)<65535 and start<0xffffffff and length<0xffffffff,'ZIP32 directory limit exceeded')
   z.write(struct.pack('<IHHHHIIH',0x06054b50,0,0,len(central),len(central),length,start,0))
  checksum=digest(archive);(output/'SHA256SUMS').write_text(checksum+'  '+archive.name+'\n',encoding='utf-8')
 return archive,checksum
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'dist');args=parser.parse_args();p,h=build(ROOT,args.output);print(p.name,h)
