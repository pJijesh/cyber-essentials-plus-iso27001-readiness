# Preparing for the Cyber Essentials Plus technical test

The Plus audit checks, on your real systems, that the requirements you declared are in place. This page describes what the NCSC test specification and IASME describe, and a practical preparation routine. The test specification version read for this page was v3.2 (April 2025). The requirements moved to v3.3 in April 2026, and a v3.3 test specification was not found when this page was written, so ask your Certification Body which test specification and rules they are applying. See [sources.md](sources.md).

## What the test involves

| Test | What happens | What fails it |
| --- | --- | --- |
| External vulnerability scan | The assessor identifies your internet-facing addresses (including cloud-hosted servers) and scans them with an approved tool. Each service gets a pass or fail. | Exposed services with serious known vulnerabilities, exposed administration interfaces, weak or default credentials on reachable services. |
| Authenticated vulnerability scan of sampled devices | A sample of user devices, servers and cloud-hosted servers is scanned with credentials. | A vulnerability that is critical or high (vendor rating), CVSS v3 base score 7 or more, or has no vendor rating, where a fix has been available for more than 14 days. |
| Malware protection checks | Test files are delivered by email and by browser download, and the assessor checks that protection acts. Update status of anti-malware is checked, or allow listing is tested. | Protection absent, out of date, or not blocking the test files. |
| MFA check | The assessor signs in to cloud services with an organisation account from an untrusted device or private session. | No MFA prompt. |
| Account separation | A standard user tries to run an administrative action. | The action runs without a separate administrator credential. |

Every cloud service in scope is tested with at least one standard user and one administrative user. Any failed sub-test fails its test case and the overall assessment, although the specification lets the Certification Body pass minor deviations (under 5 percent of tests) where there is no sign of a wider problem. Check whether that tolerance still applies.

## How the sample is chosen

- The sample must be representative of your device types and builds. Standardised builds can reduce the number of devices that need testing.
- IASME describes the audit as covering a representative set of user devices, all internet gateways, and all servers that offer services to unauthenticated internet users, with a random sample of typically around 10 percent of systems, after which the assessor decides whether more testing is needed.
- The assessor works out the sample size using the Certification Body's method and keeps the calculation as evidence.
- One reseller page lists minimum sample sizes by device group (1 device: 1; 2 to 5: 2; 6 to 19: 3; 20 to 60: 4; 61 or more: 5) and says the assessor selects devices randomly. That table is from a secondary source and is not attributed to IASME or the NCSC. Treat it as indicative and ask your Certification Body for theirs.
- IASME says the assessor may visit the head office and a sample of other offices. The test specification read does not set out whether tests are on site or remote, so ask your Certification Body. For a multi-site group, expect samples to span sites and countries.

## Timing and retests

- The IASME Plus page says the audit must be completed within three months of the last basic Cyber Essentials certification. Verify the current window with your Certification Body.
- IASME's April 2026 announcement says the self-assessment must be completed, finalised and unchanged before Plus testing starts, and that adjustments based on Plus results are not allowed.
- For update management, IASME states that if the initial sample fails, the organisation must fix the problem and be retested on the original sample plus a new random sample, and that a second failure revokes the underlying certificate.
- One consultancy states that the fix must be applied across all in-scope devices within 30 days of the failure. This is not stated on the IASME pages read, and another source gave no deadline. Confirm the retest window in writing before you rely on any number.

## Preparation routine

Start at least 6 to 8 weeks before you intend to certify, because patch cycles and exceptions take time.

1. **Freeze the scope and inventory.** Every device in the inventory is a candidate for the sample. Unknown devices are the most common surprise. Use the checklist items CE-SCO-03 and CE-UPD-07.
2. **Run your own authenticated vulnerability scan** of all in-scope devices and servers, and your own external scan of all public addresses. Use a tool that rates by vendor severity and CVSS v3. Do not rely on the patching tool's own report alone.
3. **Patch to the 14 day rule.** Install critical and high updates within 14 days of release, for operating systems, firmware, applications, browser extensions and plug-ins. Where an update bundle contains any critical or high fix, install the whole bundle.
4. **Deal with stragglers.** List devices that were offline, on leave, in storage or at remote sites and bring them up to date or remove them from the scope with justification.
5. **Remove unsupported software.** Remove it, or isolate the device in a separated sub-set with no internet access. Check the isolation really blocks internet traffic.
6. **Check MFA on every cloud service** with a clean browser session, including free tiers and administrator accounts. Record services that genuinely have no MFA option.
7. **Check account separation.** Standard users must be prompted for separate credentials for administrative actions.
8. **Test malware protection.** Confirm protection is active and current on all device types, including servers and macOS machines.
9. **Prepare evidence.** Keep the scan outputs, patch compliance reports, and a change log so you can show what was fixed and when.
10. **Brief the sites.** Local IT needs to know that devices may be selected, that remote access may be needed, and who to call.

## What fails most often

Based on the requirements and the test design, these are the areas to check first. They reflect where the tests are strict, not a measured failure rate.

1. Missing critical or high updates older than 14 days, especially on third-party applications, browser extensions, router and firewall firmware, and devices that are rarely online.
2. Unsupported operating systems or applications still in scope.
3. MFA not enforced on a cloud service, or guest, service and unapproved accounts that were overlooked.
4. Administrative accounts used for everyday work, so account separation fails.
5. Anti-malware out of date or missing on servers and non-Windows devices.
6. Exposed administration interfaces or open legacy ports found by the external scan.
7. A scope that does not match what is actually on the network.

## Enforcing endpoint controls

Several of these controls (update rings, disk and firewall settings, compliance checks) can be enforced centrally rather than checked by hand. The author's companion repository [intune-endpoint-baseline](https://github.com/pJijesh/intune-endpoint-baseline) shows one way to do this for Windows and macOS with Microsoft Intune, mapped to the five Cyber Essentials themes. It is an example only. Nothing in this repository depends on it.
