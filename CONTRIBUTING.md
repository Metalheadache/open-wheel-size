# Contributing

Use the issue templates for specifications, missing packages, applicability or
source/attribution concerns. Include stable identity, exact market/year/trim,
front and rear separately, source URL and page/table locator, explicit unknowns,
and the rights basis for the material you submit. Do not claim “verified” without
supporting review evidence. Do not paste private reviewer details or credentials.

Code/docs contributions are under MIT. Data/compilation contributions you control
are proposed under CC BY 4.0, with compatible third-party attribution preserved.
Do not submit material you lack rights to contribute on those terms. Research
purpose and citation alone do not supply those rights. Report concerns via issues
without posting private legal correspondence or personal details.

Do not manually edit the canonical public projection as a competing master.
Submit a correction proposal to the maintainer; accepted changes are reconciled
with the canonical source and release eligibility before a projection is generated.
Public acceptance is not downstream production approval.

Run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`.
The workflow needs no secrets and has read-only permissions. Pull requests must
never execute in a privileged publish context. Release publication is manual,
after clean-history/content review, using an unused immutable version tag.
See [RELEASING.md](RELEASING.md).
