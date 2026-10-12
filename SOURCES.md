# Sources and attribution

All 2,390 public source citations are preserved in the [sources table](data/sources-001.jsonl.gz),
with title, publisher, version, dates, public URL and captured-content hash.
Original permissions, scope and attribution requirements are in the separately
keyed [source rights table](data/source_rights-001.jsonl.gz).
The [source manifest](source-manifest.json) pins both tables and their checksums.

No source documents or copied raw passages are included. Citation is not permission;
the original unknown/notPermitted labels have not been upgraded. Each claim carries
its exact source key and page/table/section locator. Source date and retrieval date
are not inferred vehicle model years.

Print all source references offline:

```python
import gzip, json
with gzip.open("data/sources-001.jsonl.gz", "rt", encoding="utf-8") as stream:
    for line in stream:
        source = json.loads(line)
        print(source["source_key"], source["publisher"], source["reference_url"])
```

Representative references (the table above contains every source):

- [20-inch SPYDER black high-gloss front rim, 982601025BQ041](https://www.teile.com/en/porsche-tequipment-shop/model-cayman-982-718/37/wheels/601d-wheel-rims/219/20-inch-spyder-wheel-rim-85j-x-20-et57-black-high-gloss/134253) — TEILE.COM, independent specialist genuine Porsche parts retailer.
- [C-Class Coupe Operator's Manual](https://www.mbusa.com/content/dam/mb-nafta/us/owners/manuals/2015/operators/MY15_C-Coupe_Operator.pdf) — Mercedes-Benz USA.
- [2015 Mercedes-Benz C-Class Coupe US brochure](https://www.auto-brochures.com/makes/Mercedes_Benz/C-Class/Mercedes%20Benz_US%20C-Class-Coupe_2015.pdf) — Auto-Brochures.
- [2016 Mercedes-Benz E-Class Sedan/Wagon US brochure](https://cdn.dealereprocess.org/cdn/brochures/mercedesbenz/2016-eclass.pdf) — Dealer eProcess.
- [Megane Trophy manufacturer launch](https://media.renault.at/article/1086) — Renault / Renault Sport.
- [Megane RS Red Bull Racing edition](https://media.renault.at/586/article/1230) — Renault Austria.
- [Audi A3/S3 Australian Specifications MY24](https://media.audi.com/is/content/audi/nemo/australia/specification_guides/a3/a3_sportback/Audi_A3_S3_Specification_Guide_MY24_270923.pdf) — Audi Australia.
- [Audi A4 | S4 Sedan and Avant Australian Specifications (October 2020)](https://resource.digitaldealer.com.au/pdf/19199990860b59dbd2824a990600339.pdf) — Audi Australia (manufacturer specification sheet; Digital Dealer mirror).
- [Mercedes-Benz Australia CLA Shooting Brake specifications](https://xr793.com/wp-content/uploads/2023/10/2015-Mercedes-Benz-CLA-Shooting-Brake-AUS.pdf) — Mercedes-Benz Australia via XR793.
- [The E-Class All-Terrain, April2017 Australian manufacturer brochure](https://xr793.com/wp-content/uploads/2023/10/2017-Mercedes-Benz-E-Class-All-Terrain-AUS.pdf) — Mercedes-Benz Australia/Pacific Pty Ltd (manufacturer document mirrored by xr793.com).
- [Mitsubishi Australia Evolution VIII brochure](https://xr793.com/wp-content/uploads/2023/04/2005-Mitsubishi-Lancer-Evolution-VIII-AUS.pdf) — Mitsubishi Australia; XR793 archive.
- [Nissan Australia MY24 Z specification](https://www-asia.nissan-cdn.net/content/dam/Nissan/AU/Files/Brochures/Models/Specsheet/AU21-P00000235-06_FY24_Nissan_10_Year_Warranty_Brochure_Spec_Sheet_Updates_Z_FA.pdf) — Nissan.
- [au-rs3-2016-oem](https://xr793.com/wp-content/uploads/2023/04/2016-Audi-RS-3-Sportback-Specs-AUS.pdf) — Audi.
- [Specifications BMW 3 Series Coupé 325i 330i 335i 03/2010](https://www.press.bmwgroup.com/global/article/attachment/T0077074EN/113015) — BMW Group PressClub Global.
- [BMW MY2010 approved wheel and tyre combinations e92_2010a2_320](https://myair-bdr.bmwgroup.com/static/manual/RadReif/downloads/Rad-Reifen/mj2010/E90_E91_E92_E93/e92_2010a2_320.pdf) — BMW Group.

Preserve each source’s attribution requirement. See [NOTICE.md](NOTICE.md) for
the limited scope of the project contribution licence.
