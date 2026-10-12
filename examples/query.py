"""Offline example; prints zero packages for this tooling-only release."""
import json
from pathlib import Path
catalog = json.loads((Path(__file__).resolve().parents[1] / 'data/catalog.json').read_text(encoding='utf-8'))
for package in catalog['packages']:
    print(package['package_key'], package['market'], package['configuration_reference'])
print('Packages:', len(catalog['packages']))
