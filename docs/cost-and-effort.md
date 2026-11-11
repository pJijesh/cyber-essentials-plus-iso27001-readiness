# Cost and effort planning outline

This page gives a structure for estimating cost and effort. It deliberately quotes no prices. Scheme fees and Certification Body charges change, vary by organisation size and complexity, and could not be verified from authoritative sources to a standard suitable for publication here. Obtain current written quotes.

What the public pages do say, as checked on 11 November 2026: the NCSC page states that Cyber Essentials is priced by organisation size and that Cyber Essentials Plus is priced according to the size and complexity of the network. IASME publishes its own price information and states that Plus is quoted individually. Read the current pages instead of relying on a figure from this repository.

## Cost categories

| Category | Cyber Essentials | Cyber Essentials Plus | ISO/IEC 27001 |
| --- | --- | --- | --- |
| Scheme or certification fees | Assessment fee for the verified self-assessment, set by size | Audit fee, quoted per network size and complexity, plus travel if on site | Stage 1 and Stage 2 audit days, yearly surveillance, recertification at three years |
| Advice and consultancy | Optional Certification Body support or Cyber Advisor help | Optional pre-assessment | Optional gap analysis, risk method, internal auditor training |
| Technology | MFA licences, patching and device management, anti-malware, firewall replacement | Vulnerability scanning tool, patch automation | Logging, backup, endpoint, vulnerability and access tools, as risks require |
| Internal effort | IT, security, finance and HR time | IT time during sample tests and remediation | Wide: leadership, risk owners, HR, facilities, procurement, internal audit |
| Remediation | Retiring unsupported systems, closing exposed services | Re-patching after a failed sample, retest | Corrective actions from audits |
| Ongoing | Annual renewal | Annual renewal and a new test | Surveillance audits, internal audits, management reviews, awareness training |

## Effort drivers

- **Number of legal entities and sites.** Each adds scoping, evidence and sampling work.
- **Countries and languages.** Evidence collection, interviews and local legal advice take longer.
- **Device count and diversity.** Standard builds reduce Plus sampling and patching effort. A mixed estate raises both.
- **Current maturity.** Mature central management of devices and identity is the biggest saving. Use the `score` output to estimate it.
- **Legacy systems.** Unsupported software needs replacement or isolation projects, which often dominate the budget.
- **Cloud footprint.** More services means more MFA and configuration checks, and more third parties to review.
- **Existing documentation.** Starting from nothing makes the ISMS documents a large effort.
- **Management time.** Leadership review, risk acceptance and internal audit need scheduled senior time.

## A simple estimating method

1. Run `init` and `score` to count gaps by theme. Each not started or partial item is a work package.
2. For each work package record owner, effort in days, external cost and dependency. Group them by theme and by site tier.
3. Add fixed items: assessment or audit days from quotes, scanning tools, training, internal audit.
4. Add contingency. A common planning practice is to hold a reserve for remediation after test failures. Choose a percentage that your finance team accepts and record the reasoning. No figure is given here.
5. Split cost between one-off and recurring so the annual run cost is visible.
6. Review against the timeline in [sequence-and-timeline.md](sequence-and-timeline.md) and check for peaks in team workload.

## Questions to ask suppliers

- What is included in the quote: number of audit days, remote or on-site, sample size, one retest?
- How are fees affected by number of sites, entities and devices?
- What happens if a test fails and when must the retest happen?
- Which test specification and rules version will be applied?
- For ISO: is the certification body accredited, and how are multi-site audits planned and charged?

## Benefits that are not on the invoice

Fewer incidents, faster customer security questionnaires, simpler insurance conversations and better asset knowledge. Record the ones that matter to your organisation, but do not present them as guaranteed outcomes.
