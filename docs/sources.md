# Sources and verification status

All checks were made on **11 November 2026**. Pages were read through a web fetch tool that returns summaries of the page content, so wording was not compared character by character against the originals. Everything in this repository is paraphrased. Nothing is quoted from the standard, the NCSC documents or vendor material.

Source types used below:

- **Primary**: a public page or document published by the NCSC, IASME or ISO (including the ISO catalogue pages).
- **Secondary**: certification bodies, consultancies, resellers and vendor blogs. Useful, but not authoritative.
- **Not verified**: from general knowledge, not confirmed in a source during this check.

## Cyber Essentials

| Fact | Where used | Source type | Source |
| --- | --- | --- | --- |
| Requirements for IT Infrastructure is at v3.3, dated April 2026 | data, docs | Primary | NCSC PDF, `ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf` |
| Five technical themes: firewalls, secure configuration, security update management, user access control, malware protection | data, docs | Primary | NCSC Cyber Essentials overview page and the v3.3 document |
| Detail of requirements (default passwords, admin interfaces, inbound rules, device locking, 14 day updates and the CVSS 7 rule, MFA, separate admin accounts, password rules, anti-malware or allow listing) | `ce-requirements.csv` | Primary | NCSC v3.3 document |
| v3.3 changes: cloud service definition, cloud cannot be excluded from scope, FIDO2 counts as MFA, software security code of practice, untrusted connection scope wording removed, backup guidance emphasised | docs | Primary | NCSC v3.3 document and IASME April 2026 article |
| Scope rules: BYOD, home working, routers, third-party accounts, sub-sets, bespoke software | scoping guide | Primary | NCSC v3.3 document |
| v3.3 applies to assessment accounts created from about 27 April 2026; accounts created earlier have six months to certify under the earlier requirements | docs | Primary | IASME articles. One reading gave the cut-off as after 26 April and another as 27 April, so check the exact date if it matters |
| Question set named Danzell, published 13 February 2026 | docs | Primary | IASME article |
| MFA enabled wherever a cloud service offers it, free or paid, is an automatic fail if missing; two new automatic fail questions for 14 day installation of critical and high updates (operating systems and firmware, and applications) | scoring priority list | Primary | IASME April 2026 article |
| Unsupported software in scope is an automatic fail | scoring priority list | Primary | IASME FAQ page |
| Certificates last 12 months | docs | Primary | IASME FAQ page |
| Point in time is the certificate issue date; all legal entities in scope are listed; declaration covers the whole period | docs | Primary | IASME April 2026 article |

## Cyber Essentials Plus

| Fact | Where used | Source type | Source |
| --- | --- | --- | --- |
| Test cases: external scan, authenticated patch scan of a sample, malware checks, MFA check, account separation; every cloud service tested with a standard and an admin user; sample must be representative; standard builds can reduce the sample; deviations under 5 percent may be passed at the Delivery Partner's discretion | CE+ test page | Primary | NCSC Cyber Essentials Plus test specification **v3.2** (April 2025). A v3.3 version was not found, so details may have changed |
| Audit covers a representative set of user devices, all internet gateways and servers offering unauthenticated services; typical sample about 10 percent; head office and other offices may be visited | CE+ test page | Primary | IASME Cyber Essentials Plus page |
| Plus audit must be completed within three months of the last basic certification | docs, roadmap diagram | Primary, supported by secondary | IASME Plus page and IASME FAQ (a recent basic certificate lets you skip the self-assessment questions). Repeated by other certification bodies. Verify at booking time |
| Self-assessment must be finalised and unchanged before Plus testing; update management retest uses original sample plus a new random sample; second failure revokes the certificate | CE+ test page | Primary | IASME April 2026 article |
| Remediation within 30 days of a failed sample | CE+ test page (flagged) | Secondary only | One consultancy page. Not found on IASME pages and another source gave no deadline. Treat as unverified |
| Minimum sample sizes by device group (1, 2, 3, 4, 5) | CE+ test page (flagged as indicative) | Secondary only | One reseller page, not attributed to IASME or the NCSC |

## ISO/IEC 27001

| Fact | Where used | Source type | Source |
| --- | --- | --- | --- |
| ISO/IEC 27001:2022 is edition 3, published October 2022; Amendment 1:2024 "Climate action changes" exists | docs | Primary | ISO catalogue page (committee.iso.org mirror) and the amendment catalogue entry |
| Amendment 1 affects clauses 4.1 and 4.2 and was published in February 2024 | scoping guide, roadmap | Secondary | Standards catalogue listing for the amendment |
| ISO/IEC 27002:2022 is edition 3, 2022 | docs | Primary | ISO catalogue page |
| Annex A has 93 controls in four themes; counts 37 organisational, 8 people, 14 physical, 34 technological | data, docs, tests | Secondary, two lists cross-checked | Two independent public lists agreed on every control number and title, and one listed the theme counts. The ISO catalogue pages read did not state the number |
| 2013 edition had 114 controls in 14 categories; 11 controls are new in 2022 | roadmap | Secondary | Certification body page and a consultancy summary |
| Control numbers A.5.1 to A.5.37, A.6.1 to A.6.8, A.7.1 to A.7.14, A.8.1 to A.8.34 | data, tests | Secondary | Same two lists |
| Clause structure 4 to 10 (context, leadership, planning, support, operation, performance evaluation, improvement) and the 2022 splits of 9.2 and 9.3 | roadmap | Secondary | Compliance vendor clause summary and certification body page |
| Clauses 6.1.2 and 6.1.3, Statement of Applicability content, internal audit and management review inputs | roadmap | Not verified against the standard | The standard is paywalled and was not read. Described from general knowledge of the standard and consistent with the secondary summaries. Check against the standard before writing documents |
| Certification to the 2013 edition ended on 31 October 2025 | roadmap | Secondary | Certification body and consultancy pages. Who set the date was not stated |
| Stage 1, Stage 2, annual surveillance, three year cycle, recertification | roadmap | Secondary | Certification body page |
| All Annex A short titles in this repository | data | Author's wording | Written as short paraphrases of the control names |

## Not verified

- Whether a Cyber Essentials Plus test specification newer than v3.2 has been published, and what it says about retests.
- The exact cut-off date for v3.3 accounts (26 or 27 April 2026).
- Prices for any scheme or audit. None are quoted.
- Whether the NCSC document was revised after April 2026. Files dated later in the year appeared under the same v3.3 name, and no newer version number was found.
- The CE to Annex A mapping, which is the author's judgement.
- The software has been run only on synthetic data.

## Links

- NCSC Cyber Essentials: `https://www.ncsc.gov.uk/cyberessentials/overview`
- NCSC requirements v3.3: `https://www.ncsc.gov.uk/files/cyber-essentials-requirements-for-it-infrastructure-v3-3.pdf`
- NCSC Plus test specification v3.2: `https://ncsc.gov.uk/files/cyber-essentials-plus-test-specification-v3-2.pdf`
- IASME April 2026 changes: `https://iasme.co.uk/articles/upcoming-changes-to-the-cyber-essentials-scheme-april-2026/`
- IASME important update on the April 2026 changes: `https://iasme.co.uk/?p=27103`
- IASME Cyber Essentials Plus: `https://www.iasme.co.uk/cyberessentials/cyber-essentials-plus/`
- IASME FAQ: `https://www.iasme.co.uk/frequently-asked-questions`
- ISO/IEC 27001 catalogue entry: `https://www.iso.org/standard/27001`
