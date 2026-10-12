# Data dictionary

Public projection schema 1.0; dataset package 0.1.1; source intake schema 1.2.
All properties are required; null marks missing optional values. No arbitrary extra fields.
CSV cells use JSON scalar encoding: `null`, `true`, `false`, numbers, or quoted strings.
Parse a CSV cell with `json.loads` to recover the exact scalar.

Stable keys retain source identity. Explicit front/rear rows must exist for every package.
Nominal tyre section width is not measured section width; OEM geometry is not fitment approval.
Claims retain field-level source keys and locators, states and evidence labels.
The current tables contain zero rows; this schema does not imply data availability.

## axles

| Field | Type / values | Unit / semantics |
|---|---|---|
| actual_section_width_mm | ["number", "null"] | millimetres (measured) |
| axle | ["front", "rear"] |  |
| evidence_grade | "string" |  |
| load_index | ["string", "null"] |  |
| measuring_rim_width_in | ["number", "null"] | inches |
| offset_mm | ["number", "null"] | millimetres (signed) |
| package_key | "string" |  |
| run_flat | [true, false, null] |  |
| source_key | "string" |  |
| source_locator | "string" |  |
| spacer_mm | ["number", "null"] | millimetres |
| speed_rating | ["string", "null"] |  |
| tyre_aspect_ratio_percent | ["number", "null"] | percent |
| tyre_brand | ["string", "null"] |  |
| tyre_model | ["string", "null"] |  |
| tyre_rim_diameter_in | ["number", "null"] | inches |
| tyre_section_width_mm | ["number", "null"] | millimetres (nominal) |
| wheel_diameter_in | ["number", "null"] | inches |
| wheel_part_number | ["string", "null"] |  |
| wheel_width_in | ["number", "null"] | inches |
| xl_reinforced | [true, false, null] |  |

## claims

| Field | Type / values | Unit / semantics |
|---|---|---|
| canonical_unit | ["string", "null"] |  |
| claim_key | "string" |  |
| entity_key | "string" |  |
| entity_type | "string" |  |
| evidence_grade | "string" |  |
| field_path | "string" |  |
| source_key | "string" |  |
| source_locator | "string" |  |
| state | ["known", "unknown", "notApplicable"] |  |
| unknown_reason | ["string", "null"] | Explicit reason when value is unknown or notApplicable |
| value | ["string", "number", "boolean", "null"] |  |
| value_type | ["string", "number", "boolean"] |  |

## packages

| Field | Type / values | Unit / semantics |
|---|---|---|
| configuration_reference | ["string", "null"] |  |
| market | ["string", "null"] |  |
| model_year_end | ["number", "null"] | Manufacturer model year only; both null or a complete interval |
| model_year_start | ["number", "null"] | Manufacturer model year only; both null or a complete interval |
| option_package_code | ["string", "null"] |  |
| package_key | "string" |  |
| package_name | "string" |  |
| package_type | ["string", "null"] |  |
| reference_year | ["number", "null"] | Dated configuration year; not inferred model year |
| region | ["string", "null"] |  |
| source_key | "string" |  |
| source_locator | "string" |  |
| variant_key | "string" |  |
| wheel_style_code | ["string", "null"] |  |
| year_basis | ["manufacturerModelYear", "datedConfiguration", "undatedConfiguration"] |  |

## platforms

| Field | Type / values | Unit / semantics |
|---|---|---|
| chassis_generation | "string" |  |
| manufacturer | "string" |  |
| model_family | "string" |  |
| platform_key | "string" |  |

## reviews

| Field | Type / values | Unit / semantics |
|---|---|---|
| application_promotion_status | ["notAssessed"] |  |
| entity_key | "string" |  |
| entity_type | "string" |  |
| garage_support | ["notAssessed"] |  |
| public_release_basis | "string" | Public scoped rationale, no private reviewer details |
| public_release_status | ["eligible"] |  |
| technical_review_status | ["unreviewed", "inReview", "accepted", "rejected", "blocked"] | Independent of redistribution eligibility |

## sources

| Field | Type / values | Unit / semantics |
|---|---|---|
| attribution | "string" |  |
| content_hash | ["string", "null"] |  |
| contribution_license | "string" |  |
| public_release_basis | "string" | Public scoped rationale, no private reviewer details |
| publication_date | ["string", "null"] |  |
| publisher | "string" |  |
| reference_url | "string" |  |
| retrieval_date | ["string", "null"] |  |
| source_key | "string" |  |
| source_version | "string" |  |
| title | "string" |  |

## variants

| Field | Type / values | Unit / semantics |
|---|---|---|
| aliases_en | ["string", "null"] |  |
| aliases_zh | ["string", "null"] |  |
| body_style | ["string", "null"] |  |
| configuration_reference | ["string", "null"] |  |
| drive_type | ["string", "null"] |  |
| engine_code | ["string", "null"] |  |
| market | ["string", "null"] |  |
| model_year_end | ["number", "null"] | Manufacturer model year only; both null or a complete interval |
| model_year_start | ["number", "null"] | Manufacturer model year only; both null or a complete interval |
| platform_key | "string" |  |
| reference_year | ["number", "null"] | Dated configuration year; not inferred model year |
| region | ["string", "null"] |  |
| transmission_name | ["string", "null"] |  |
| transmission_type | ["string", "null"] |  |
| trim | "string" |  |
| variant_key | "string" |  |
| year_basis | ["manufacturerModelYear", "datedConfiguration", "undatedConfiguration"] |  |
