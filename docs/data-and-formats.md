# Data files and formats

## Reference data (`data/`)

| File | Columns | Content |
| --- | --- | --- |
| `ce-requirements.csv` | `id`, `theme`, `requirement`, `applies_to`, `evidence_examples`, `common_failure` | 45 checklist items in plain English: 8 scope and inventory, then the five technical themes (8 firewalls, 6 secure configuration, 7 security update management, 12 user access control, 4 malware protection). Written in the author's words from the NCSC requirements v3.3 and the IASME 2026 announcements. Items marked "Practical measure" (CE-UPD-07, CE-MAL-04) are good practice that help you evidence a requirement and are not separate scheme requirements. |
| `iso27001-annexa.csv` | `id`, `theme`, `short_title` | All 93 Annex A controls with short titles in the author's words. Themes: Organisational 37, People 8, Physical 14, Technological 34. No descriptive text from the standard is reproduced. |
| `mapping-ce-to-iso.csv` | `ce_id`, `annexa_id`, `strength`, `note` | One row per CE item and Annex A control it contributes to, with `strong` or `partial`, plus one `none` row (empty `ce_id`) for each of the 63 Annex A controls with no CE item, explaining why. |

The mapping is judgement, not an official crosswalk. `strong` means the CE item addresses a main part of the control. It never means the control is satisfied.

## Assessment workbook

Created by `python -m readiness init`. One row per item.

| Column | Meaning |
| --- | --- |
| `id` | A CE id (for example `CE-FW-01`) or Annex A id (for example `A.8.8`) |
| `status` | `not started`, `partial`, `implemented` or `not applicable` (case and underscores are tolerated, `n/a` is accepted) |
| `owner` | A role or name, free text |
| `evidence_ref` | Where the evidence is kept, for example a ticket or document reference |
| `last_reviewed` | Date evidence was last checked, `YYYY-MM-DD` |
| `notes` | Free text. For `not applicable` it must hold a justification of at least 10 characters. For an included Annex A control it is used as the Statement of Applicability reason |

`init --with-titles` adds a `title` column for readability. It is ignored when scoring. Every item for each included scope must have a row. Problems stop the run and are all listed together with line numbers.

## Scoring rule

Implemented counts 1, partial counts 0.5, not started counts 0. Not applicable items leave the denominator. Coverage is the weighted total divided by the number of applicable items. The percentage is a progress indicator, not a pass mark: Cyber Essentials has automatic fail areas that a high percentage can hide, which is why they are listed separately in the report.

## Outputs of `score`

| File | Content |
| --- | --- |
| `report.md` | Summary, coverage by theme, automatic fail areas, gaps, evidence hygiene, not applicable items |
| `report.json` | The same data for other tools |
| `soa.csv`, `soa.md` | Draft Statement of Applicability |

Exit status: 0 success, 2 input problem, 3 coverage under `--fail-under`.

## Sites input and outputs

`sites.csv` columns: `site`, `country`, `headcount`, `data_sensitivity` (low, medium, high), `regulated_data` (no, unknown, yes), `it_maturity` (low, medium, high), `connectivity` (poor, adequate, good), and optional `local_requirements_note`. The allowed values come from the config file.

Outputs of `sites`: `site-tiers.csv`, `sites-report.md`, `sites.json`, `tier-control-sets.csv`. See [proportionate-controls.md](proportionate-controls.md).
