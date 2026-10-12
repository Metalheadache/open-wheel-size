# open-wheel-size

An open, source-attributed vehicle wheel and tyre reference catalog for research,
comparison and tool development, with explicit market, model-year and axle scope.
Independently maintained as an alternative in the wheel-size reference category;
not an official Wheel-Size.com product, mirror, API-compatible clone or
manufacturer-endorsed database.

**v1.0.0 publishes the complete sanitized structured research catalog:**
621 platform/generation keys, 6,349 market/year/trim variants, 11,771 OEM packages,
23,542 front/rear axle records, 2,390 sources and 732,391 claims. It also preserves
all 21,087 historical review records, 1,278 effective enrichment facts, 19,533
sanitized provenance records, eight corrections and nine scoped known issues.
The reconciliation report preserves 924 missing field-level axle claim links; no
values are corrected or promoted during publication. See generated [coverage](COVERAGE.md), including completeness, markets and years.

**Unresolved rights labels are preserved. Publication makes no claim of legal
clearance, technical approval or downstream production approval.** The owner
explicitly authorized publishing structured facts despite unresolved rights labels.
Source-material copying permissions remain 2,355 `unknown` and 35 `notPermitted`.
Those labels concern their original scope; they neither grant permissions nor
by themselves decide rights in independently recorded facts. [Scope and notices](NOTICE.md).

[中文](README.zh-CN.md) · [Dictionary](DATA_DICTIONARY.md) · [Sources](SOURCES.md) ·
[Methodology](METHODOLOGY.md) · [Contributing](CONTRIBUTING.md)

Download the archive and SHA256SUMS from [Releases](https://github.com/Metalheadache/open-wheel-size/releases),
or clone this repository. Python 3.9+ and its standard library suffice; no account,
network, hosted database or third-party package is needed after download.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 examples/query.py --market CN --limit 5
python3 scripts/release.py --output dist
```

Primary files are deterministic UTF-8 JSON Lines compressed with gzip, indexed by
`data/index.json`. Each row is one JSON object. The release additionally contains
lossless CSV.gz tables: parse each CSV cell as JSON to preserve nulls and types.
The complete master remains private; this is its versioned, allowlisted projection,
not a raw database dump or a second manually edited canonical dataset.

```python
import gzip, json
with gzip.open("data/axles-001.jsonl.gz", "rt", encoding="utf-8") as stream:
    first_axle = json.loads(next(stream))
    print(first_axle["package_key"], first_axle["axle"], first_axle["offset_mm"])
```

Hierarchy: manufacturer → platform/generation → scoped variant → OEM package →
front/rear axle. Dimensions are numeric inches, millimetres or percent. Null
represents missing data, never zero. Claims preserve unknown reasons, positive N/A,
original evidence grades and field-level sources/locators. Historical unknown claims
can coexist with newer known claims; current canonical wheel values are in `axles`.
Hardware claims remain in `claims`. Known issues qualify affected records.

Reference years are not automatically manufacturer model years. Chinese aliases
are not China-market specifications; GLOBAL is not country availability. Nominal
tyre width is not measured width. OEM geometry is not aftermarket fitment approval.

Original code, schemas, tests and documentation: [MIT](LICENSE-CODE).
Owner-controlled eligible data/compilation contributions: [CC BY 4.0](LICENSE-DATA).
Third-party rights are not relicensed, and unknown permissions remain unknown.
Research is the project purpose, not a licence restriction or an exemption.
Retain attribution and source-specific notices; see [NOTICE.md](NOTICE.md).

Public eligibility, technical review, downstream production promotion and
Apply-to-Garage support are distinct. Public contributions must not automatically
promote production data. Consumers should use a reviewed pinned release/hash through
their importer and signing pipeline; never treat mutable main as a runtime authority.
No application integration is supplied. [Stable handoff mapping](COMPATIBILITY.md).

This catalog is maintained for research, comparison and software development.
It may contain incomplete, unreviewed or incorrect records. Inclusion of a
specification is not confirmation of aftermarket fitment, brake clearance,
dynamic clearance or vehicle safety. Refer to the cited sources and perform
appropriate vehicle-specific verification.

Use issue templates for corrections, missing vehicles/packages, market/year
applicability and source/attribution concerns. Do not submit private information,
credentials, copied source documents or unsupported “verified” labels.
