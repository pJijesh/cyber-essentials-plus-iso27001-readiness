# Readiness report

Workbook: assessment.csv. As-of date: 2026-11-11. Evidence review interval: 365 days.

> This report is a planning aid based on self-reported status. It is not an assessment, an audit or a certification decision. Cyber Essentials is a baseline subset of what ISO/IEC 27001 expects, so certification to one does not imply the other. Check requirements against the current published scheme documents.

Scoring rule: implemented 1.0, partial 0.5, not started 0.0, not applicable excluded.

## Summary

| Scope | Items | Applicable | Implemented | Partial | Not started | Not applicable | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Cyber Essentials | 45 | 44 | 24 | 16 | 4 | 1 | 72.7% |
| ISO/IEC 27001 Annex A | 93 | 87 | 14 | 38 | 35 | 6 | 37.9% |

## Coverage by theme

### Cyber Essentials

| Theme | Items | Implemented | Partial | Not started | Not applicable | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| Scope and inventory | 8 | 5 | 2 | 1 | 0 | 75.0% |
| Firewalls | 8 | 4 | 4 | 0 | 0 | 75.0% |
| Secure configuration | 6 | 4 | 2 | 0 | 0 | 83.3% |
| Security update management | 7 | 0 | 4 | 3 | 0 | 28.6% |
| User access control | 12 | 8 | 4 | 0 | 0 | 83.3% |
| Malware protection | 4 | 3 | 0 | 0 | 1 | 100.0% |

### ISO/IEC 27001 Annex A

| Theme | Items | Implemented | Partial | Not started | Not applicable | Coverage |
| --- | --- | --- | --- | --- | --- | --- |
| Organisational | 37 | 3 | 13 | 21 | 0 | 25.7% |
| People | 8 | 2 | 4 | 2 | 0 | 50.0% |
| Physical | 14 | 3 | 7 | 4 | 0 | 46.4% |
| Technological | 34 | 6 | 14 | 8 | 6 | 46.4% |

## Cyber Essentials automatic fail areas

These items are treated as automatic failures by the scheme as of the April 2026 changes (see docs/sources.md). Close any gap here before booking an assessment.

| Id | Requirement | Why it matters | Status |
| --- | --- | --- | --- |
| CE-UAC-04 | Turn on MFA for every cloud service that offers it, whether the option is free, bundled or paid. | MFA not enabled on a cloud service that offers it is an automatic fail | partial |
| CE-UPD-01 | Make sure all in-scope software is licensed and still supported by its vendor. | Unsupported software in scope is an automatic fail | partial |
| CE-UPD-02 | Remove software that has gone out of support, or take the device out of scope using a separated network sub-set that has no internet access. | Unsupported software in scope is an automatic fail | not started |
| CE-UPD-04 | Install operating system and firmware updates within 14 days of release when they fix vulnerabilities rated critical or high, scored 7 or more on CVSS v3, or have no severity given. | Critical or high operating system and firmware updates must be installed within 14 days | partial |
| CE-UPD-05 | Install application updates, including browser extensions and plug-ins, within 14 days of release under the same severity rules. | Critical or high application updates must be installed within 14 days | partial |

## Gaps

93 items are not started or partial. 5 of them are automatic fail areas and are listed first.

| Id | Scope | Theme | Item | Status | Owner | Priority | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CE-UPD-02 | Cyber Essentials | Security update management | Remove software that has gone out of support, or take the device out of scope using a separated network sub-set that has no internet access. | not started | Endpoint Engineer | auto fail area | Two legacy shop-floor PCs run an operating system that is out of support. Isolation design agreed but not yet built. |
| CE-UPD-01 | Cyber Essentials | Security update management | Make sure all in-scope software is licensed and still supported by its vendor. | partial | Endpoint Engineer | auto fail area | All supported except the two legacy shop-floor PCs (see CE-UPD-02). |
| CE-UPD-04 | Cyber Essentials | Security update management | Install operating system and firmware updates within 14 days of release when they fix vulnerabilities rated critical or high, scored 7 or more on CVSS v3, or have no severity given. | partial | Endpoint Engineer | auto fail area | Operating systems meet the 14 day target through update rings. Firmware on branch routers is not yet tracked. |
| CE-UPD-05 | Cyber Essentials | Security update management | Install application updates, including browser extensions and plug-ins, within 14 days of release under the same severity rules. | partial | Endpoint Engineer | auto fail area | Browsers and office applications are covered. Browser extensions and the CAD plug-ins are not. |
| CE-UAC-04 | Cyber Essentials | User access control | Turn on MFA for every cloud service that offers it, whether the option is free, bundled or paid. | partial | IT Manager | auto fail area | MFA enforced on the email and collaboration suite and the ERP portal. Two supplier portals and one workflow app still use passwords only. Plan to enforce or retire by end of January. |
| CE-SCO-07 | Cyber Essentials | Scope and inventory | If anything is excluded, justify the exclusion, explain how it is separated from the rest, and list every legal entity that is in scope. | not started | IT Manager |  | Mexico plant network shares a wireless segment with a contractor. Segregation not yet in place, so the site is not ready to be in scope. |
| CE-UPD-03 | Cyber Essentials | Security update management | Turn on automatic updates wherever the product offers them. | not started | unassigned |  |  |
| CE-UPD-06 | Cyber Essentials | Security update management | If an update bundles several fixes and any one is critical or high, install the whole bundle within 14 days. | not started | Endpoint Engineer |  |  |
| CE-SCO-04 | Cyber Essentials | Scope and inventory | List every cloud service that holds or processes organisational data, who is responsible for each control (you or the provider), and keep all of them in scope. | partial | IT Manager |  | Register covers the main cloud tenant. Plant level and supplier-hosted services still to be added. |
| CE-SCO-08 | Cyber Essentials | Scope and inventory | Bring accounts used by suppliers, contractors and managed service providers into scope, and any organisation-owned device lent to a third party. | partial | IT Manager |  |  |
| CE-FW-01 | Cyber Essentials | Firewalls | Protect every in-scope device with a correctly configured firewall: a boundary firewall, or a firewall on the device itself. | partial | Network Engineer |  |  |
| CE-FW-04 | Cyber Essentials | Firewalls | Block unauthenticated inbound connections by default and only open what is needed. | partial | Network Engineer |  |  |
| CE-FW-05 | Cyber Essentials | Firewalls | Have each inbound rule approved and documented by an authorised person, with the business reason recorded. | partial | Network Engineer |  |  |
| CE-FW-08 | Cyber Essentials | Firewalls | For cloud services, use the provider's network and data flow controls (for example access rules and allow lists) where a firewall cannot be used. | partial | Network Engineer |  | Storage account network rules reviewed for the main tenant only. |
| CE-CFG-02 | Cyber Essentials | Secure configuration | Change default or easily guessed passwords on every device and application. | partial | IT Manager |  |  |
| CE-CFG-04 | Cyber Essentials | Secure configuration | Turn off auto-run features that start files without the user choosing to. | partial | IT Manager |  |  |
| CE-UPD-07 | Cyber Essentials | Security update management | Practical measure: be able to show which in-scope devices are missing critical or high updates older than 14 days, including devices that are offline. | partial | Endpoint Engineer |  | Dashboard covers managed laptops only. Servers and plant PCs are reported by hand. |
| CE-UAC-06 | Cyber Essentials | User access control | Use separate administrator accounts for administration only, never for email, web browsing or everyday work. | partial | IT Manager |  |  |
| CE-UAC-07 | Cyber Essentials | User access control | Take away special privileges when they are no longer needed, for example after a change of role. | partial | IT Manager |  |  |
| CE-UAC-10 | Cyber Essentials | User access control | Help people choose unique passwords, for example by providing a password manager and guidance on long passphrases, and do not force routine expiry. | partial | IT Manager |  |  |
| A.5.3 | ISO/IEC 27001 Annex A | Organisational | Separation of conflicting duties | not started | Security Lead |  |  |
| A.5.4 | ISO/IEC 27001 Annex A | Organisational | Management duty to enforce security | not started | Security Lead |  |  |
| A.5.5 | ISO/IEC 27001 Annex A | Organisational | Contact with authorities | not started | Security Lead |  |  |
| A.5.7 | ISO/IEC 27001 Annex A | Organisational | Threat intelligence | not started | Security Lead |  | No threat intelligence source subscribed yet. |
| A.5.8 | ISO/IEC 27001 Annex A | Organisational | Security in project work | not started | Security Lead |  |  |
| A.5.10 | ISO/IEC 27001 Annex A | Organisational | Acceptable use rules | not started | Security Lead |  |  |
| A.5.15 | ISO/IEC 27001 Annex A | Organisational | Access control rules | not started | Security Lead |  |  |
| A.5.20 | ISO/IEC 27001 Annex A | Organisational | Security terms in supplier agreements | not started | unassigned |  |  |
| A.5.22 | ISO/IEC 27001 Annex A | Organisational | Supplier service monitoring and change | not started | Security Lead |  |  |
| A.5.23 | ISO/IEC 27001 Annex A | Organisational | Cloud service security | not started | Security Lead |  |  |
| A.5.24 | ISO/IEC 27001 Annex A | Organisational | Incident management planning | not started | Security Lead |  | Incident plan to be written after the risk assessment. |
| A.5.25 | ISO/IEC 27001 Annex A | Organisational | Assessing security events | not started | Security Lead |  |  |
| A.5.26 | ISO/IEC 27001 Annex A | Organisational | Incident response | not started | Security Lead |  |  |
| A.5.27 | ISO/IEC 27001 Annex A | Organisational | Learning from incidents | not started | Security Lead |  |  |
| A.5.28 | ISO/IEC 27001 Annex A | Organisational | Evidence collection | not started | unassigned |  |  |
| A.5.29 | ISO/IEC 27001 Annex A | Organisational | Security during disruption | not started | unassigned |  |  |
| A.5.30 | ISO/IEC 27001 Annex A | Organisational | ICT continuity readiness | not started | Security Lead |  | Continuity plan covers the main plant only. |
| A.5.32 | ISO/IEC 27001 Annex A | Organisational | Intellectual property | not started | Security Lead |  |  |
| A.5.33 | ISO/IEC 27001 Annex A | Organisational | Records protection | not started | Security Lead |  |  |
| A.5.34 | ISO/IEC 27001 Annex A | Organisational | Privacy and personal data protection | not started | Security Lead |  |  |
| A.5.35 | ISO/IEC 27001 Annex A | Organisational | Independent security review | not started | Security Lead |  |  |
| A.6.3 | ISO/IEC 27001 Annex A | People | Awareness and training | not started | HR Manager |  |  |
| A.6.8 | ISO/IEC 27001 Annex A | People | Security event reporting | not started | HR Manager |  |  |
| A.7.5 | ISO/IEC 27001 Annex A | Physical | Environmental and physical threats | not started | Facilities Manager |  |  |
| A.7.7 | ISO/IEC 27001 Annex A | Physical | Clear desk and clear screen | not started | unassigned |  |  |
| A.7.8 | ISO/IEC 27001 Annex A | Physical | Equipment siting and protection | not started | Facilities Manager |  |  |
| A.7.10 | ISO/IEC 27001 Annex A | Physical | Storage media | not started | unassigned |  |  |
| A.8.3 | ISO/IEC 27001 Annex A | Technological | Information access restriction | not started | IT Manager |  |  |
| A.8.10 | ISO/IEC 27001 Annex A | Technological | Information deletion | not started | unassigned |  |  |
| A.8.16 | ISO/IEC 27001 Annex A | Technological | Monitoring activities | not started | IT Manager |  |  |
| A.8.18 | ISO/IEC 27001 Annex A | Technological | Privileged utility programs | not started | IT Manager |  |  |
| A.8.21 | ISO/IEC 27001 Annex A | Technological | Network service security | not started | IT Manager |  |  |
| A.8.22 | ISO/IEC 27001 Annex A | Technological | Network segregation | not started | IT Manager |  |  |
| A.8.23 | ISO/IEC 27001 Annex A | Technological | Web filtering | not started | unassigned |  |  |
| A.8.24 | ISO/IEC 27001 Annex A | Technological | Cryptography use | not started | IT Manager |  |  |
| A.5.1 | ISO/IEC 27001 Annex A | Organisational | Information security policies | partial | Security Lead |  | Policy set drafted and awaiting board approval. |
| A.5.2 | ISO/IEC 27001 Annex A | Organisational | Security roles and responsibilities | partial | Security Lead |  | Security lead named. Site level roles not yet defined. |
| A.5.6 | ISO/IEC 27001 Annex A | Organisational | Contact with specialist security groups | partial | Security Lead |  |  |
| A.5.9 | ISO/IEC 27001 Annex A | Organisational | Inventory of information and assets | partial | Security Lead |  |  |
| A.5.11 | ISO/IEC 27001 Annex A | Organisational | Return of assets on exit | partial | Security Lead |  |  |
| A.5.12 | ISO/IEC 27001 Annex A | Organisational | Information classification | partial | Security Lead |  |  |
| A.5.16 | ISO/IEC 27001 Annex A | Organisational | Identity lifecycle management | partial | Security Lead |  |  |
| A.5.18 | ISO/IEC 27001 Annex A | Organisational | Access rights provisioning and review | partial | Security Lead |  |  |
| A.5.19 | ISO/IEC 27001 Annex A | Organisational | Security in supplier relationships | partial | Security Lead |  |  |
| A.5.21 | ISO/IEC 27001 Annex A | Organisational | ICT supply chain security | partial | Security Lead |  |  |
| A.5.31 | ISO/IEC 27001 Annex A | Organisational | Legal and contractual requirements | partial | Security Lead |  |  |
| A.5.36 | ISO/IEC 27001 Annex A | Organisational | Compliance with own policies and standards | partial | Security Lead |  |  |
| A.5.37 | ISO/IEC 27001 Annex A | Organisational | Documented operating procedures | partial | Security Lead |  |  |
| A.6.4 | ISO/IEC 27001 Annex A | People | Disciplinary process | partial | HR Manager |  |  |
| A.6.5 | ISO/IEC 27001 Annex A | People | Duties after leaving or role change | partial | HR Manager |  |  |
| A.6.6 | ISO/IEC 27001 Annex A | People | Confidentiality agreements | partial | HR Manager |  |  |
| A.6.7 | ISO/IEC 27001 Annex A | People | Remote working | partial | HR Manager |  |  |
| A.7.3 | ISO/IEC 27001 Annex A | Physical | Securing offices and rooms | partial | Facilities Manager |  |  |
| A.7.4 | ISO/IEC 27001 Annex A | Physical | Physical monitoring | partial | Facilities Manager |  | CCTV at the main plant and design studio. Other sites rely on alarms only. |
| A.7.6 | ISO/IEC 27001 Annex A | Physical | Working in secure areas | partial | Facilities Manager |  |  |
| A.7.9 | ISO/IEC 27001 Annex A | Physical | Assets off premises | partial | Facilities Manager |  |  |
| A.7.12 | ISO/IEC 27001 Annex A | Physical | Cabling security | partial | Facilities Manager |  |  |
| A.7.13 | ISO/IEC 27001 Annex A | Physical | Equipment maintenance | partial | Facilities Manager |  |  |
| A.7.14 | ISO/IEC 27001 Annex A | Physical | Secure disposal or reuse | partial | Facilities Manager |  |  |
| A.8.1 | ISO/IEC 27001 Annex A | Technological | User endpoint devices | partial | IT Manager |  |  |
| A.8.2 | ISO/IEC 27001 Annex A | Technological | Privileged access rights | partial | IT Manager |  |  |
| A.8.5 | ISO/IEC 27001 Annex A | Technological | Secure authentication | partial | IT Manager |  |  |
| A.8.8 | ISO/IEC 27001 Annex A | Technological | Technical vulnerability management | partial | IT Manager |  |  |
| A.8.11 | ISO/IEC 27001 Annex A | Technological | Data masking | partial | IT Manager |  |  |
| A.8.12 | ISO/IEC 27001 Annex A | Technological | Data leakage prevention | partial | IT Manager |  |  |
| A.8.13 | ISO/IEC 27001 Annex A | Technological | Backup | partial | IT Manager |  | Backups run for the main plant systems. Restore tests not yet recorded. |
| A.8.15 | ISO/IEC 27001 Annex A | Technological | Logging | partial | IT Manager |  | Central logging for identity and email only. |
| A.8.19 | ISO/IEC 27001 Annex A | Technological | Software installation on production systems | partial | IT Manager |  |  |
| A.8.20 | ISO/IEC 27001 Annex A | Technological | Network security | partial | IT Manager |  |  |
| A.8.26 | ISO/IEC 27001 Annex A | Technological | Application security requirements | partial | IT Manager |  |  |
| A.8.27 | ISO/IEC 27001 Annex A | Technological | Secure architecture principles | partial | IT Manager |  |  |
| A.8.32 | ISO/IEC 27001 Annex A | Technological | Change management | partial | IT Manager |  |  |
| A.8.34 | ISO/IEC 27001 Annex A | Technological | Protecting systems during audit testing | partial | IT Manager |  |  |

## Evidence and review hygiene

### Overdue evidence reviews (19)

| Id | Item | Owner | Last reviewed | Days overdue |
| --- | --- | --- | --- | --- |
| A.8.6 | Capacity management | IT Manager | 2025-08-19 | 84 |
| A.6.1 | Background screening | HR Manager | 2025-08-20 | 83 |
| CE-MAL-01 | Have a malware protection method active on every in-scope device. | Endpoint Engineer | 2025-08-25 | 78 |
| CE-SCO-08 | Bring accounts used by suppliers, contractors and managed service providers into scope, and any organisation-owned device lent to a third party. | IT Manager | 2025-08-26 | 77 |
| A.8.1 | User endpoint devices | IT Manager | 2025-09-02 | 70 |
| CE-SCO-06 | Cover home and remote working: devices used at home are in scope, and a router supplied by the organisation is in scope. | IT Manager | 2025-09-06 | 66 |
| CE-FW-05 | Have each inbound rule approved and documented by an authorised person, with the business reason recorded. | Network Engineer | 2025-09-14 | 58 |
| CE-UAC-03 | Remove or disable accounts when they are no longer needed, for example when someone leaves or after a set period of inactivity. | IT Manager | 2025-10-02 | 40 |
| A.5.16 | Identity lifecycle management | Security Lead | 2025-10-06 | 36 |
| A.8.19 | Software installation on production systems | IT Manager | 2025-10-07 | 35 |
| A.5.12 | Information classification | Security Lead | 2025-10-08 | 34 |
| A.5.21 | ICT supply chain security | Security Lead | 2025-10-09 | 33 |
| CE-CFG-01 | Regularly remove or disable accounts that are not needed, including guest, default and unused administrator accounts. | IT Manager | 2025-10-11 | 31 |
| CE-FW-03 | Do not expose firewall administration pages to the internet unless there is a documented business need and either MFA or an allow list of trusted addresses is in place. | Network Engineer | 2025-10-22 | 20 |
| A.7.2 | Physical entry controls | Facilities Manager | 2025-10-22 | 20 |
| A.7.13 | Equipment maintenance | Facilities Manager | 2025-10-24 | 18 |
| A.8.2 | Privileged access rights | IT Manager | 2025-10-26 | 16 |
| CE-UAC-08 | Where passwords are used, protect against guessing with MFA, throttling (no more than 10 guesses in 5 minutes) or lockout after no more than 10 failures. | IT Manager | 2025-11-05 | 6 |
| CE-FW-08 | For cloud services, use the provider's network and data flow controls (for example access rules and allow lists) where a firewall cannot be used. | Network Engineer | 2025-11-06 | 5 |

### Implemented or partial with no review date (3)

| Id | Item | Owner |
| --- | --- | --- |
| CE-SCO-05 | Decide whether personal devices (BYOD) may access organisational data. Those that do are in scope; keep a list or block them. | IT Manager |
| A.5.18 | Access rights provisioning and review | Security Lead |
| A.7.9 | Assets off premises | Facilities Manager |

### Implemented or partial with no evidence reference (5)

| Id | Item | Status | Owner |
| --- | --- | --- | --- |
| CE-FW-07 | Run a software firewall on devices that are used on untrusted networks such as home or public Wi-Fi. | implemented | Network Engineer |
| CE-CFG-05 | Make sure users are authenticated before they can reach organisational data or services. | implemented | IT Manager |
| CE-MAL-01 | Have a malware protection method active on every in-scope device. | implemented | Endpoint Engineer |
| A.5.11 | Return of assets on exit | partial | Security Lead |
| A.8.13 | Backup | partial | IT Manager |

## Not applicable items (7)

Each exclusion needs a justification that an assessor or auditor will accept.

| Id | Scope | Item | Justification |
| --- | --- | --- | --- |
| CE-MAL-03 | Cyber Essentials | If using application allow listing, only approved, validly signed applications may run, the approved list is kept current, and users cannot install unsigned ones. | Anti-malware software is used on every in-scope device, so allow listing is not relied on. |
| A.8.4 | ISO/IEC 27001 Annex A | Source code access | The group holds no bespoke source code. It buys packaged software only. |
| A.8.25 | ISO/IEC 27001 Annex A | Secure development lifecycle | No software is developed in house or by suppliers for the group. |
| A.8.28 | ISO/IEC 27001 Annex A | Secure coding | No software is developed in house or by suppliers for the group. |
| A.8.29 | ISO/IEC 27001 Annex A | Security testing before release | No software is developed in house or by suppliers for the group. |
| A.8.30 | ISO/IEC 27001 Annex A | Outsourced development oversight | No software development is outsourced. |
| A.8.31 | ISO/IEC 27001 Annex A | Separate development, test and live | No development environments exist. Packaged software is configured in production under change control. |
