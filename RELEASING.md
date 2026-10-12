# Releasing

The public dataset version is 1.0.1 and the portable schema is 2.0. They are separate
from the source intake schema version. Never overwrite tags or existing assets.

Privately reconcile the canonical ledger, preserve source input hashes and update
the scoped publication authorization. Generate into a new staging directory:

```sh
python3 scripts/project.py --ledger PATH_TO_RECONCILED_LEDGER --output STAGING_DIRECTORY --private-report PRIVATE_AUDIT_JSON
```

The projector is the single schema allowlist. It never edits the master and never
promotes rights flags. Audit redactions and excluded fields privately; never copy
its private report, original ledger or source attachments into public Git. Refresh
manifest, coverage and source metadata from the projected rows, inspect the entire
staged allowlist and all history being pushed, then run:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/release.py --output dist
```

Choose an unused release version, update manifest/changelog/citation, and verify the
authenticated GitHub owner and existing repository. Example after configuring CLI
authentication locally and inspecting the proposed commit:

```sh
gh api user --jq .login
gh repo view Metalheadache/open-wheel-size
git diff --cached
git log --oneline --all
# Substitute the NEW unused version, never an existing tag:
git tag NEW_TAG
git push origin main NEW_TAG
gh release create NEW_TAG dist/open-wheel-size-NEW_VERSION.zip dist/SHA256SUMS --notes-file RELEASE_NOTES.md
```

Use a clean unauthenticated clone and download of the published archive. Run the
validator/tests and rebuild the archive; compare SHA256SUMS and internal file hashes.
Inspect GitHub source ZIP/tar archives, public history, CI logs and asset lists.
Retain unresolved rights labels and explicitly avoid claims of legal clearance.
The repository workflow uses no publishing credentials or privileged PR execution.

Version 1.0.1 stores tagged JSONL.gz inputs directly in a ZIP with fixed headers.
It does not regenerate compressed convenience tables: gzip compression can vary
with the runtime library. Version 1.0.0 CSV assets remain historical convenience
exports; their decoded values match all JSON records. Do not replace those assets.
