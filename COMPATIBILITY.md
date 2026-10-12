# Canonical version and stable identity mapping

`manifest.json` pins the complete private source v1 by all seven input hashes and
import batch `47fc2ad9-1250-5c4c-8e27-ad7eff5d357b`. No private input is bundled.
Every projected master row carries its original `record_id` and `stable_id` where
available. Stable entity keys, claim keys and relationships are unchanged.

Stable ID contract: UUIDv5 namespace `ab384916-c7c1-5f61-a4ef-718432d32720`, name
`canonical_json([kind, exact_original_key])`, UTF-8, sorted object keys, compact
separators. Axle keys are `[package_key, axle]`. Never rekey a dated correction or
guess an existing downstream application ID. Some auxiliary rows have no proposed
entity ID; their original record UUID remains the identity. Rights rows share the
source identity; known-issue IDs are the original issue labels.

Public payload hashes differ from private hashes because of allowlisting/date/null
normalization. Public schema 2.0 and dataset version 1.0.0 are separate from the
original intake schema 1.2. The dataset contains all structured canonical factual
records, not all private attachments, review notes or planning/layout history.
Sanitized provenance may omit private fields while retaining identity and states.

A consumer should import a reviewed pinned release/projection through its existing
importer and signing pipeline. Public research coverage and production coverage may
differ. Public inclusion does not approve production publication; omitted private
fields remain in the original master. No runtime main-branch fetch, application
migration, production activation or Apply-to-Garage support is supplied.
