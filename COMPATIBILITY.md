# Canonical compatibility

`manifest.json` pins the complete private source v1 by workbook SHA-256 and import
batch ID. It records zero included IDs. The source files remain private; their
hashes permit an authorized consumer to verify the exact common input.

Stable ID contract: UUIDv5 namespace `ab384916-c7c1-5f61-a4ef-718432d32720`, name
`canonical_json([kind, exact_original_key])`, UTF-8, sorted object keys and compact
separators. Kinds are source, platform, variant, package, axle and claim. Axle keys
are `[package_key, axle]`. Never rekey dated corrections or guess application IDs.
Public projection keys must retain the original identity; public payload hashes
will differ after sanitization and must never impersonate private payload hashes.

The public schema covers the wheel/tyre projection, not a lossless dump of all
private hardware/review records. A future nonempty release must record any omitted
fields and keep conflict dependencies. No compatibility with a third-party API is
claimed. Production consumers should use a reviewed, pinned release/projection via
their existing importer/signing process. Public and production coverage can differ;
public exclusions do not remove private master records. No runtime main-branch
fetch, production activation, database migration or Garage support is provided.
