# open-wheel-size

An independently maintained vehicle wheel and tyre reference catalog for research,
comparison and tool development, with explicit market, model-year and axle scope.

**DATA RELEASE BLOCKED — tooling and documentation only.** This first package
contains **zero vehicle records**. The complete private research v1 has not been
released. Its source-material flags do not establish an open redistribution basis
for the independently recorded facts; that separate assessment is still missing.
See [coverage](COVERAGE.md) and [release eligibility](METHODOLOGY.md).

This project is an independent alternative in the wheel-size reference catalog
category. It is not an official Wheel-Size.com product, mirror, API-compatible
clone, or manufacturer-endorsed database.

[中文说明](README.zh-CN.md) · [Dictionary](DATA_DICTIONARY.md) ·
[Sources](SOURCES.md) · [Contributing](CONTRIBUTING.md) · [Notices](NOTICE.md)

Download the versioned package from this repository's **Releases** page. A ZIP of
this source tree also works. Python 3.9 or later is sufficient; no account,
database, credentials, third-party Python packages or network is needed:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 examples/query.py
python3 scripts/release.py --output dist
```

`data/catalog.json` is the deterministic UTF-8 public projection. It is generated
from the private canonical catalog through a release gate, not maintained as a
second manually edited source. The current projection is intentionally empty.
The release builder emits JSON and CSV tables, schema, dictionary, coverage,
source manifest and SHA-256 checksums in a reproducible archive. Zero CSV rows
are not sample or placeholder vehicle coverage.

Hierarchy: manufacturer → platform/generation → market/year/trim variant → OEM
wheel/tyre package → separate front and rear axle records. Claims cite individual
sources and locators. Dimensions use numeric inches or millimetres; tyre aspect
ratio uses percent. Null means unknown, never zero. Positive not-applicable and
conflicting claims remain explicit. Chinese aliases do not establish China-market
specifications. Reference year and manufacturer model year are distinct.

Source evidence and technical review are independent of public-release eligibility.
An unreviewed/conflicting record may be publishable when its redistribution basis
is documented; an accurate record may still lack that basis. Public contribution
acceptance never automatically approves any downstream production catalog.
Consumers should pin a version and hash and apply their own review/import/signing
pipeline; never use a mutable main branch as a runtime authority. No application
or Garage integration is included. [Stable mapping](COMPATIBILITY.md).

Original tooling, schemas, tests and documentation are MIT licensed in
[LICENSE-CODE](LICENSE-CODE). The owner's eligible data/compilation contributions
are offered under CC BY 4.0 in [LICENSE-DATA](LICENSE-DATA), subject to the exact
scope in [NOTICE.md](NOTICE.md). No third-party documents or vehicle data are
licensed by this empty release. Research describes the purpose, not a use
restriction or permission exemption.

This catalog is maintained for research, comparison and software development.
It may contain incomplete, unreviewed or incorrect records. Inclusion of a
specification is not confirmation of aftermarket fitment, brake clearance,
dynamic clearance or vehicle safety. Refer to the cited sources and perform
appropriate vehicle-specific verification.

Submit corrections, missing packages, applicability problems or source/rights
concerns through the repository's issue templates. Do not submit private details,
credentials, source attachments or copied passages without permission.
