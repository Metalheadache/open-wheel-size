# Releasing

This package is prepared as `v0.1.1`, a tooling-only release. Reserve `v1.0.0` for
an appropriate future data release. Schema versions are independent.

1. Reconcile the canonical master and record scoped public-release eligibility.
   Generate a new allowlisted projection; never copy private history/attachments.
2. Regenerate coverage, source manifest and manifest hashes, preserving source
   identity. Inspect all staged files and every commit to be pushed.
3. Run the offline commands below twice and compare archive/checksum bytes.
4. Verify the authenticated owner and existing repository, refs, tags and releases.
   Never force-push or replace an existing tag/asset. Upload only allowlisted files.
5. Tag the reviewed commit, publish the versioned archive and checksums, then use
   a clean unauthenticated download to rerun validation and compare all checksums.
   Inspect CI logs and release assets. Report actual status, not intent.

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
python3 scripts/release.py --output dist
# Optional authenticated GitHub CLI, after configuring it yourself:
gh api user --jq .login
gh repo view Metalheadache/open-wheel-size
git status --short
git diff --cached
git log --oneline --all
# Only after confirming this version/tag is unused and the commit is reviewed:
git tag v0.1.1
git push origin main v0.1.1
gh release create v0.1.1 dist/open-wheel-size-0.1.1.zip dist/SHA256SUMS --title '0.1.1 — tooling only; data release blocked' --notes-file RELEASE_NOTES.md
```

For the next release, update the version in the manifest, changelog and citation,
then use that unused tag and generated asset name. If the data gate is still
blocked, retain the blocker and zero counts; do not imply a complete data release.
