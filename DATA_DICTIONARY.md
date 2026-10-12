# Data dictionary

Dataset 1.0.0; public row schema 2.0; source intake schema 1.2.
The schema has closed field allowlists. UTF-8 JSON Lines are gzip compressed with
zero timestamps. `data/index.json` pins compressed and uncompressed SHA-256 hashes.
CSV cells are JSON-encoded, including null, arrays and objects; parse with json.loads.

`record_id` maps the exact original master row; `stable_id` is the original proposed
entity UUID where available. Keys retain their original strings. Blank scalar cells
become null, and date wrappers become their recorded ISO dates. No numeric facts
or original rights/review labels are changed. Legacy claim-year qualifiers may be
strings; variant/package years and geometric dimensions are numeric.

Claims include wheel, tyre and hardware fields. `state` retains known, unknown and
notApplicable. Field paths carry units/axle scope; canonical_unit is preserved.
`stage2Accepted` and similar research grades do not mean production approval.
Current axle values can coexist with older unknown claims. See known_issues.

Provenance retains allowed structured state/value/link fields, not private review
prose. Numeric provenance keys are array positions in the original export; original
record UUIDs disambiguate them. Internal-path provenance keys become null.
Qualification tags summarize technical caveats without reproducing private notes.

## axles

| Field | JSON type | Units / meaning |
|---|---|---|
| actual_section_width_mm | ['number', 'null'] | millimetres, measured |
| axle | ['string', 'number', 'boolean', 'null'] |  |
| evidence_grade | ['string', 'number', 'boolean', 'null'] |  |
| load_index | ['string', 'number', 'boolean', 'null'] |  |
| measuring_rim_width_in | ['number', 'null'] | inches |
| offset_mm | ['number', 'null'] | millimetres, signed |
| package_key | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| run_flat | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| spacer_mm | ['number', 'null'] | millimetres |
| speed_rating | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| tyre_aspect_ratio_percent | ['number', 'null'] | percent |
| tyre_brand | ['string', 'number', 'boolean', 'null'] |  |
| tyre_model | ['string', 'number', 'boolean', 'null'] |  |
| tyre_rim_diameter_in | ['number', 'null'] | inches |
| tyre_section_width_mm | ['number', 'null'] | millimetres, nominal |
| wheel_diameter_in | ['number', 'null'] | inches |
| wheel_part_number | ['string', 'number', 'boolean', 'null'] |  |
| wheel_width_in | ['number', 'null'] | inches |
| xl_reinforced | ['string', 'number', 'boolean', 'null'] |  |

## claims

| Field | JSON type | Units / meaning |
|---|---|---|
| axle | ['string', 'number', 'boolean', 'null'] |  |
| brake_package | ['string', 'number', 'boolean', 'null'] |  |
| canonical_unit | ['string', 'number', 'boolean', 'null'] |  |
| claim_key | ['string', 'number', 'boolean', 'null'] |  |
| drivetrain | ['string', 'number', 'boolean', 'null'] |  |
| entity_key | ['string', 'number', 'boolean', 'null'] |  |
| entity_type | ['string', 'number', 'boolean', 'null'] |  |
| evidence_grade | ['string', 'number', 'boolean', 'null'] |  |
| field_path | ['string', 'number', 'boolean', 'null'] |  |
| market | ['string', 'number', 'boolean', 'null'] |  |
| model_year_end | ['string', 'number', 'boolean', 'null'] |  |
| model_year_start | ['string', 'number', 'boolean', 'null'] |  |
| original_unit | ['string', 'number', 'boolean', 'null'] |  |
| package_code | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| region | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| state | ['string', 'number', 'boolean', 'null'] |  |
| suspension_package | ['string', 'number', 'boolean', 'null'] |  |
| trim | ['string', 'number', 'boolean', 'null'] |  |
| unknown_reason | ['string', 'number', 'boolean', 'null'] |  |
| value | ['string', 'number', 'boolean', 'null'] |  |
| value_type | ['string', 'number', 'boolean', 'null'] |  |

## corrections

| Field | JSON type | Units / meaning |
|---|---|---|
| accepted_at | ['string', 'number', 'boolean', 'null'] |  |
| application_status | ['string', 'number', 'boolean', 'null'] |  |
| axle | ['string', 'number', 'boolean', 'null'] |  |
| correction_id | ['string', 'number', 'boolean', 'null'] |  |
| entity_key | ['string', 'number', 'boolean', 'null'] |  |
| evidence_ref | ['string', 'number', 'boolean', 'null'] |  |
| field | ['string', 'number', 'boolean', 'null'] |  |
| impacted_fact_ids | ['array', 'null'] |  |
| old_value | ['string', 'number', 'boolean', 'null'] |  |
| proposed_value | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| source_sha256 | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| value | ['string', 'number', 'boolean', 'null'] |  |

## effective_facts

| Field | JSON type | Units / meaning |
|---|---|---|
| applicability | object |  |
| axle | ['string', 'number', 'boolean', 'null'] |  |
| axle_stable_id | ['string', 'null'] |  |
| batch_id | ['string', 'number', 'boolean', 'null'] |  |
| canonical_unit | ['string', 'number', 'boolean', 'null'] |  |
| capture_sha256 | ['string', 'number', 'boolean', 'null'] |  |
| claim_stable_id | ['string', 'null'] |  |
| entity_key | ['string', 'number', 'boolean', 'null'] |  |
| evidence_group | ['string', 'number', 'boolean', 'null'] |  |
| fact_id | ['string', 'number', 'boolean', 'null'] |  |
| field | ['string', 'number', 'boolean', 'null'] |  |
| gap_id | ['string', 'number', 'boolean', 'null'] |  |
| qualifications | array |  |
| record_id | ['string', 'null'] |  |
| review_status | ['string', 'number', 'boolean', 'null'] |  |
| source_id | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| supporting_evidence | array |  |
| table | ['string', 'number', 'boolean', 'null'] |  |
| value | ['string', 'number', 'boolean', 'null'] |  |

## known_issues

| Field | JSON type | Units / meaning |
|---|---|---|
| affected_keys | ['array', 'null'] |  |
| finding | ['string', 'number', 'boolean', 'null'] |  |
| issue_id | ['string', 'number', 'boolean', 'null'] |  |
| limitation | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| source_reference | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| status | ['string', 'number', 'boolean', 'null'] |  |
| subject | ['string', 'number', 'boolean', 'null'] |  |

## packages

| Field | JSON type | Units / meaning |
|---|---|---|
| brake_package_applicability | ['string', 'number', 'boolean', 'null'] |  |
| brake_package_key | ['string', 'number', 'boolean', 'null'] |  |
| configuration_reference | ['string', 'number', 'boolean', 'null'] |  |
| market | ['string', 'number', 'boolean', 'null'] |  |
| model_year_end | ['number', 'null'] |  |
| model_year_start | ['number', 'null'] |  |
| option_package_code | ['string', 'number', 'boolean', 'null'] |  |
| package_key | ['string', 'number', 'boolean', 'null'] |  |
| package_name | ['string', 'number', 'boolean', 'null'] |  |
| package_type | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| reference_year | ['number', 'null'] |  |
| region | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| suspension_package_applicability | ['string', 'number', 'boolean', 'null'] |  |
| suspension_package_key | ['string', 'number', 'boolean', 'null'] |  |
| transmission_applicability | ['string', 'number', 'boolean', 'null'] |  |
| variant_key | ['string', 'number', 'boolean', 'null'] |  |
| wheel_style_code | ['string', 'number', 'boolean', 'null'] |  |
| year_basis | ['string', 'number', 'boolean', 'null'] |  |

## platforms

| Field | JSON type | Units / meaning |
|---|---|---|
| aliases_en | ['string', 'number', 'boolean', 'null'] |  |
| aliases_zh | ['string', 'number', 'boolean', 'null'] |  |
| chassis_generation | ['string', 'number', 'boolean', 'null'] |  |
| manufacturer | ['string', 'number', 'boolean', 'null'] |  |
| model_family | ['string', 'number', 'boolean', 'null'] |  |
| platform_key | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| stable_id | ['string', 'null'] |  |

## provenance

| Field | JSON type | Units / meaning |
|---|---|---|
| applicability | object |  |
| applicability_state | ['string', 'number', 'boolean', 'null'] |  |
| axle | ['string', 'number', 'boolean', 'null'] |  |
| canonical_record_sha256 | ['string', 'number', 'boolean', 'null'] |  |
| capture_sha256 | ['string', 'number', 'boolean', 'null'] |  |
| cell_id | ['string', 'number', 'boolean', 'null'] |  |
| dependency_claim_id | ['string', 'number', 'boolean', 'null'] |  |
| dependency_fact_id | ['string', 'number', 'boolean', 'null'] |  |
| dependency_fact_ids | ['array', 'null'] |  |
| entity_key | ['string', 'number', 'boolean', 'null'] |  |
| event_id | ['string', 'number', 'boolean', 'null'] |  |
| fact_id | ['string', 'number', 'boolean', 'null'] |  |
| field | ['string', 'number', 'boolean', 'null'] |  |
| field_dictionary_version | ['string', 'number', 'boolean', 'null'] |  |
| hardware_cell_id | ['string', 'number', 'boolean', 'null'] |  |
| inventory_id | ['string', 'number', 'boolean', 'null'] |  |
| next_state | ['string', 'number', 'boolean', 'null'] |  |
| original_field_path | ['string', 'number', 'boolean', 'null'] |  |
| previous_state | ['string', 'number', 'boolean', 'null'] |  |
| provenance_key | ['string', 'number', 'boolean', 'null'] |  |
| qualifications | array |  |
| record_id | ['string', 'null'] |  |
| review_status | ['string', 'number', 'boolean', 'null'] |  |
| source_id | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| source_locator | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| status | ['string', 'number', 'boolean', 'null'] |  |
| supporting_evidence | array |  |
| table | ['string', 'number', 'boolean', 'null'] |  |
| unallocated_existing_claim_id | ['string', 'number', 'boolean', 'null'] |  |
| unit | ['string', 'number', 'boolean', 'null'] |  |
| value | ['string', 'number', 'boolean', 'null'] |  |
| variant_key | ['string', 'number', 'boolean', 'null'] |  |

## reviews

| Field | JSON type | Units / meaning |
|---|---|---|
| blocking_issue_count | ['number', 'null'] |  |
| entity_key | ['string', 'number', 'boolean', 'null'] |  |
| entity_type | ['string', 'number', 'boolean', 'null'] |  |
| publication_status | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| research_status | ['string', 'number', 'boolean', 'null'] |  |
| rights_review_status | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| technical_review_status | ['string', 'number', 'boolean', 'null'] |  |

## source_rights

| Field | JSON type | Units / meaning |
|---|---|---|
| attribution_requirement | ['string', 'number', 'boolean', 'null'] |  |
| commercial_use_permission | ['string', 'number', 'boolean', 'null'] |  |
| licence_status | ['string', 'number', 'boolean', 'null'] |  |
| permitted_use_description | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| redistribution_permission | ['string', 'number', 'boolean', 'null'] |  |
| rights_checked_at | ['string', 'number', 'boolean', 'null'] |  |
| rights_reference_url | ['string', 'number', 'boolean', 'null'] |  |
| rights_scope | ['string', 'number', 'boolean', 'null'] |  |
| rights_source_locator | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |

## sources

| Field | JSON type | Units / meaning |
|---|---|---|
| attribution_requirement | ['string', 'number', 'boolean', 'null'] |  |
| content_hash | ['string', 'number', 'boolean', 'null'] |  |
| issuing_organization | ['string', 'number', 'boolean', 'null'] |  |
| jurisdiction | ['string', 'number', 'boolean', 'null'] |  |
| language | ['string', 'number', 'boolean', 'null'] |  |
| market | ['string', 'number', 'boolean', 'null'] |  |
| publication_date | ['string', 'number', 'boolean', 'null'] |  |
| publisher | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| reference_url | ['string', 'number', 'boolean', 'null'] |  |
| retrieval_date | ['string', 'number', 'boolean', 'null'] |  |
| source_key | ['string', 'number', 'boolean', 'null'] |  |
| source_type | ['string', 'number', 'boolean', 'null'] |  |
| source_version | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| title | ['string', 'number', 'boolean', 'null'] |  |

## variants

| Field | JSON type | Units / meaning |
|---|---|---|
| aliases_en | ['string', 'number', 'boolean', 'null'] |  |
| aliases_zh | ['string', 'number', 'boolean', 'null'] |  |
| body_style | ['string', 'number', 'boolean', 'null'] |  |
| brake_package_display_name | ['string', 'number', 'boolean', 'null'] |  |
| brake_package_key | ['string', 'number', 'boolean', 'null'] |  |
| configuration_reference | ['string', 'number', 'boolean', 'null'] |  |
| drive_type | ['string', 'number', 'boolean', 'null'] |  |
| engine_code | ['string', 'number', 'boolean', 'null'] |  |
| engine_description | ['string', 'number', 'boolean', 'null'] |  |
| engine_family | ['string', 'number', 'boolean', 'null'] |  |
| factory_brake_package | ['string', 'number', 'boolean', 'null'] |  |
| factory_suspension_package | ['string', 'number', 'boolean', 'null'] |  |
| market | ['string', 'number', 'boolean', 'null'] |  |
| model_year_end | ['number', 'null'] |  |
| model_year_start | ['number', 'null'] |  |
| package_code | ['string', 'number', 'boolean', 'null'] |  |
| platform_key | ['string', 'number', 'boolean', 'null'] |  |
| production_end | ['string', 'number', 'boolean', 'null'] |  |
| production_start | ['string', 'number', 'boolean', 'null'] |  |
| record_id | ['string', 'null'] |  |
| reference_year | ['number', 'null'] |  |
| region | ['string', 'number', 'boolean', 'null'] |  |
| stable_id | ['string', 'null'] |  |
| suspension_package_display_name | ['string', 'number', 'boolean', 'null'] |  |
| suspension_package_key | ['string', 'number', 'boolean', 'null'] |  |
| transmission_name | ['string', 'number', 'boolean', 'null'] |  |
| transmission_type | ['string', 'number', 'boolean', 'null'] |  |
| trim | ['string', 'number', 'boolean', 'null'] |  |
| variant_key | ['string', 'number', 'boolean', 'null'] |  |
| year_basis | ['string', 'number', 'boolean', 'null'] |  |
