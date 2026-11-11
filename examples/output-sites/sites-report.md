# Site tiering report

Input: sites.csv.

> Example model for internal prioritisation. It is not legal advice and does not state what any law requires. Factors, weights, thresholds and control sets are examples to adjust to your own risk appetite.

Tiers set how much local control and assurance a site needs. They do not reduce Cyber Essentials requirements for any site inside the certified scope: every in-scope device and service must meet the scheme requirements, whatever its tier.

## Tiers

| Tier | Name | Sites | CE items | Annex A controls | Review cycle | Assurance |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Baseline | 1 | 39 | 0 | Annual | Annual self-attestation by the site lead, spot checked by group IT. |
| 2 | Enhanced | 3 | 45 | 25 | Twice a year | Annual review by group security with sampled evidence, plus a remote technical check. |
| 3 | Full | 2 | 45 | 93 | Quarterly | Internal audit in the ISMS audit programme, management review input, and independent technical testing. |

Tier descriptions:

- Tier 1 (Baseline): Small or low-exposure site. Meets the five Cyber Essentials technical themes plus an asset and cloud service register.
- Tier 2 (Enhanced): Adds the scope and third-party items and a core set of ISO management controls: policy, roles, access lifecycle, supplier and cloud oversight, training, incident reporting, backup and logging.
- Tier 3 (Full): Site inside the ISO/IEC 27001 scope. Every Annex A control is considered and the Statement of Applicability records the decision for each.

## Sites

Score is the weighted share of the maximum risk points, from 0 to 100. Tier thresholds: 35, 65.

| Site | Country | Headcount | Score | Tier by score | Floor applied | Final tier | Main drivers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ashgrove Plant | Mexico | 140 | 72.7 | 3 | none | 3 (Full) | regulated_data (12); it_maturity (8); data_sensitivity (6) |
| Northgate Works | United Kingdom | 310 | 72.7 | 3 | none | 3 (Full) | data_sensitivity (12); regulated_data (12); headcount (8) |
| Rhenmark Plant | Germany | 180 | 63.6 | 2 | none | 2 (Enhanced) | regulated_data (12); data_sensitivity (6); headcount (6) |
| Calder Design Studio | United Kingdom | 28 | 40.9 | 2 | none | 2 (Enhanced) | data_sensitivity (12); it_maturity (4); headcount (2) |
| Silvermere Assembly | Poland | 95 | 36.4 | 2 | none | 2 (Enhanced) | data_sensitivity (6); headcount (4); it_maturity (4) |
| Tidewater Sales Office | Malaysia | 12 | 31.8 | 1 | none | 1 (Baseline) | it_maturity (8); connectivity (4); headcount (2) |

## Weights

| Factor | Weight |
| --- | --- |
| headcount | 2 |
| data_sensitivity | 3 |
| regulated_data | 3 |
| it_maturity | 2 |
| connectivity | 1 |

## Local requirements notes (supplied by you)

This column is passed through from the input. The tool does not read, interpret or validate it. Complete it with local advice where an obligation may apply.

| Site | Country | Note |
| --- | --- | --- |
| Ashgrove Plant | Mexico | Not completed. Ask local counsel which obligations apply. |
| Northgate Works | United Kingdom | Example note: customer contracts require annual penetration testing. Confirm with commercial team. |
| Rhenmark Plant | Germany | Not completed. Ask local counsel which obligations apply to employee and customer data. |
| Calder Design Studio | United Kingdom | Holds unreleased product designs. Local advice not yet requested. |
| Silvermere Assembly | Poland | Not completed. |
| Tidewater Sales Office | Malaysia | not completed |

The full minimum control set for each tier is in tier-control-sets.csv.
