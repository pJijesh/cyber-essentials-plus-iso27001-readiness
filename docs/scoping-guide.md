# Scoping guide

Scope is where most avoidable problems start. A scope that is too narrow can be rejected or can mislead customers, and one that is too wide creates work for no benefit. Facts about Cyber Essentials scope below are paraphrased from the NCSC requirements document v3.3 (April 2026). Check the current document before you rely on them.

## Two scopes

| | Cyber Essentials scope | ISO/IEC 27001 ISMS scope |
| --- | --- | --- |
| Defined by | The scheme's rules, agreed with your Certification Body | You, within the standard's expectations, documented and agreed with the certification body |
| Unit | Devices, networks, cloud services and accounts that use the internet | Information, processes, locations, people and technology |
| Must include | All end-user devices that can reach in-scope data, and all cloud services holding organisational data | Whatever your boundary and risk assessment require, including interfaces and dependencies |

Keep a one page scope statement for each and a short note on why they differ.

## Cyber Essentials scope checklist

| Area | What to decide | Notes |
| --- | --- | --- |
| Whole organisation or sub-set | Certify everything, or a well-defined, separately managed sub-set | A sub-set must be separated, for example by a firewall or VLAN. Partial scope has to be justified to the assessor and the exclusions explained. A scope that leaves out end-user devices is not acceptable. |
| Users | Employees, contractors, volunteers, directors | Accounts the organisation owns are in scope, including those used by suppliers or managed service providers. |
| Devices | Servers, desktops, laptops, tablets, phones, firewalls, routers | Devices that accept connections from the internet, make connections to it, or control the flow between the two are the core. |
| Cloud services | Every service that holds or processes organisational data | Cloud services cannot be excluded under v3.3. Responsibility depends on the model (infrastructure, platform or software as a service). For software as a service you still configure it securely and own user access control. MFA is required wherever the service offers it. |
| Networks | Office networks, guest wireless, plant or operational technology networks, remote access | Wireless devices are in scope where attackers could reach them from the internet. Excluded networks must be shown to be separated. |
| BYOD | Personal devices that access organisational data | They are in scope. The NCSC document exempts devices used only for native calls, native text or an authenticator app. |
| Home working | Home devices, home routers | Home devices used for work are in scope. A router supplied by the organisation is in scope. For other routers the device firewall matters. |
| Third parties | Supplier and contractor accounts and devices | Organisation-owned accounts used by third parties are in scope. Third-party-owned devices are generally out of scope but still need to be configured safely if they touch your services. |
| Subsidiaries | Each legal entity in the scope | All entities in scope should be listed with name, address and company number. |
| Bespoke software | In-house or custom applications | Out of scope by default. Publicly available commercial web applications are in scope by default. |

## ISMS scope questions

- Which legal entities, sites and business processes are inside the boundary?
- Which information, applications and suppliers do they depend on?
- Which interfaces cross the boundary (shared networks, shared services, outsourced functions)?
- Do any climate related issues or expectations of interested parties affect the context? ISO/IEC 27001:2022 Amendment 1 (published February 2024) asks organisations to consider this in the context and interested party clauses.

## Practical guidance for groups

1. Start from the entity list, not the network diagram. Many scope errors are entities that were forgotten.
2. Decide per site whether it is inside or outside each scope, then record the reason. The `sites` command output gives a tier per site to inform that decision. It does not decide it.
3. Where a site is outside the Cyber Essentials scope, be ready to show how it is separated (firewall rules, VLAN design). If you cannot, treat it as in scope.
4. Fix the inventory early. CE-SCO-03 and CE-SCO-04 in the checklist are the foundation for patching, malware and access control evidence.
5. Re-confirm scope before each renewal. Acquisitions, new cloud services and new sites change it.

## Common scoping mistakes

- Treating shadow or free-tier cloud services as out of scope.
- Leaving out phones and tablets that read company email.
- Assuming a contractor's laptop is out of scope without a technical control stopping it reaching your data.
- Excluding a site network that shares a flat network with an in-scope site.
- Writing the ISMS scope to match what is already done rather than what the business and customers depend on.
