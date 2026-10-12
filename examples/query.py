"""Offline streaming query; no third-party dependencies or account required."""
import argparse,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import rows
p=argparse.ArgumentParser();p.add_argument('--market',default='CN');p.add_argument('--limit',type=int,default=5);a=p.parse_args()
n=0
for package in rows('packages'):
 if package['market']==a.market:
  print(package['package_key'],package['configuration_reference']);n+=1
  if n>=a.limit:break
print('Displayed packages:',n)
