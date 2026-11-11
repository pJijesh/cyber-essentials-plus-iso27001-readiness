# ISO/IEC 27001 implementation roadmap

This is a practical outline of the work, in the order it usually has to happen. The structure of the standard is paraphrased from public summaries and the ISO catalogue page. The standard itself is paywalled and was not read in full, so use it directly when you write your documents. See [sources.md](sources.md).

## Structure of the standard in brief

ISO/IEC 27001:2022 (edition 3, published October 2022) has requirement clauses 4 to 10 and Annex A.

| Clause | Theme | What you must be able to show |
| --- | --- | --- |
| 4 | Context of the organisation | The issues and interested parties that matter, and the scope of the ISMS. Amendment 1:2024 adds consideration of climate change to this context work. |
| 5 | Leadership | Top management commitment, an information security policy, and defined roles and responsibilities. |
| 6 | Planning | A risk assessment and risk treatment process, a Statement of Applicability, security objectives, and planning of changes to the ISMS. |
| 7 | Support | Resources, competence, awareness, communication and controlled documented information. |
| 8 | Operation | Carrying out the risk assessments and treatment plans, and keeping the records. |
| 9 | Performance evaluation | Monitoring and measurement, internal audit, and management review. |
| 10 | Improvement | Handling nonconformities and corrective actions, and continual improvement. |

Annex A lists 93 reference controls in four themes: organisational (37), people (8), physical (14) and technological (34). The 2022 edition reduced the 2013 total of 114 and added 11 new controls (secondary source). The standard expects you to compare your chosen controls against Annex A so that nothing necessary is missed, and to record the result in the Statement of Applicability. Certification to the 2013 edition ended on 31 October 2025 (secondary source), so new projects use the 2022 edition.

## Step by step

### 1. Scope, context and leadership (clauses 4 and 5)

- Write the ISMS scope: entities, sites, processes, systems, interfaces and exclusions with reasons.
- List interested parties and what they expect (customers, regulators, insurers, employees, owners).
- Approve an information security policy at board level and name an owner for the ISMS.
- Use the site tiers from the `sites` command to decide which locations are inside the scope.

### 2. Risk assessment method (clause 6.1.2)

Choose and document a method before you assess. It should be repeatable and give comparable results.

- Identify assets and the risks to confidentiality, integrity and availability. Asset based or scenario based approaches are both used.
- Define likelihood and impact scales, and a risk acceptance criterion approved by management.
- Assign a risk owner to each risk.
- Keep the method short enough that people will use it. A method nobody can repeat will not survive the first surveillance audit.

### 3. Risk treatment and the Statement of Applicability (clause 6.1.3)

- For each risk choose a treatment: reduce, avoid, share or accept.
- Compare the controls you intend to use with Annex A.
- Produce a Statement of Applicability listing every Annex A control with whether it is included, why, and whether it is implemented. Exclusions need a justification. The `score` command produces a draft in `soa.csv` and `soa.md`. A control marked not applicable in the workbook must carry a justification, and every included control still needs a reason linked to your risks.
- Produce a risk treatment plan with owners and dates, and have the risk owners approve it and accept residual risk.

### 4. Build the controls and the documents (clauses 7 and 8)

- Write the policies and procedures the Statement of Applicability depends on. Keep them short and usable.
- Close the Cyber Essentials gaps first. They give evidence for several technical controls (see the mapping file).
- Run awareness training and record who completed it.
- Start collecting records now: access reviews, supplier reviews, incident logs, backup restore tests, change records. Auditors sample records over time, so a control that began last week has little history.

### 5. Measure (clause 9.1)

Define a few measures that show whether the ISMS is working (for example, share of devices meeting the patch target, access review completion, incident response time). Agree who reviews them and how often.

### 6. Internal audit (clause 9.2)

- Plan an audit programme that covers the whole scope within the certification cycle.
- Use auditors who are competent and not auditing their own work.
- Report findings, agree corrective actions, and check they are closed.
- Complete at least one full internal audit before the certification audit.

### 7. Management review (clause 9.3)

- Hold a documented review by top management. Inputs include the status of actions from earlier reviews, changes in context, performance against measures, audit results, nonconformities, risk assessment results and opportunities for improvement.
- Record decisions on improvements and resources.
- Hold it before the certification audit and then at planned intervals.

### 8. Certification audit

Certification bodies use a two stage process (certification body guidance). Stage 1 reviews readiness and documentation. Stage 2 is the full assessment of the operating ISMS. After certification, annual surveillance audits follow and a recertification audit comes at the end of the three year cycle. Choose a certification body accredited by the national accreditation body (in the UK, UKAS) if your customers expect accredited certification.

### 9. Operate and improve (clause 10)

Handle nonconformities with a root cause and a corrective action. Keep the Statement of Applicability, risk register and scope up to date as the business changes. Use the `score` overdue review report to keep evidence current.

## Group notes

- Certification body guidance says larger organisations may be audited in stages across sites or units. Ask the certification body how it will plan audits across your sites.
- Make local site leads owners of local controls, and keep the Statement of Applicability at group level.
- Where legal obligations differ by country, record them in a legal and contractual requirements register with local advice. This repository does not state what any country's law requires.
