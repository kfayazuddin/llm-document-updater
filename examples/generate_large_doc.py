#!/usr/bin/env python3
"""Generates a ~10,000-word synthetic SaaS product doc (examples/sample4_large.json)
to test doc_updater.py at the scale the assignment describes. Not part of the
shipped tool -- a one-off fixture generator."""
import json
import os

INTEGRATIONS = [
    ("Salesforce", "sync leads, contacts, and opportunities in real time"),
    ("Slack", "post deployment and billing alerts directly into any channel"),
    ("Zapier", "connect Nimbus to over five thousand other apps without writing code"),
    ("HubSpot", "keep marketing and product usage data in lockstep"),
    ("Jira", "automatically open tickets when an anomaly is detected"),
    ("GitHub", "trigger deploys and roll back releases from pull request status"),
    ("Segment", "forward event streams into your existing analytics warehouse"),
    ("Snowflake", "replicate raw usage tables on an hourly schedule"),
    ("BigQuery", "run federated queries against your Nimbus data without exporting it"),
    ("Looker", "build dashboards on top of live Nimbus metrics"),
    ("Datadog", "forward infrastructure metrics and traces for unified monitoring"),
    ("PagerDuty", "route critical alerts to the right on-call engineer automatically"),
    ("Okta", "provision and deprovision Nimbus users automatically from your identity provider"),
    ("Microsoft Teams", "post deployment and billing alerts into a Teams channel"),
    ("Notion", "publish a live snapshot of key usage metrics into a shared workspace page"),
    ("Tableau", "connect Nimbus datasets directly to existing Tableau dashboards"),
    ("AWS S3", "archive raw event data to a customer-owned bucket on a nightly schedule"),
    ("Google Cloud Storage", "mirror exported reports into GCS for downstream processing"),
    ("Terraform", "manage workspaces, roles, and integrations as code"),
    ("Okta Workflows", "chain Nimbus events into broader identity automation pipelines"),
    ("Amplitude", "cross-reference product usage events with Nimbus infrastructure metrics"),
    ("Mixpanel", "correlate user behavior with billing and overage events"),
    ("ServiceNow", "open and track incident tickets from detected anomalies"),
    ("Confluence", "publish onboarding checklists and runbooks alongside live status"),
    ("Zendesk", "give support agents read-only visibility into a customer's usage history"),
    ("Stripe", "reconcile Nimbus invoices against your existing billing records"),
    ("NetSuite", "sync invoice line items into your ERP for finance reporting"),
    ("CircleCI", "gate deploys on Nimbus health checks before promoting a build"),
    ("GitLab", "mirror the GitHub integration's deploy and rollback triggers"),
    ("Splunk", "forward audit log events into an existing SIEM pipeline"),
    ("Workday", "keep employee provisioning in sync with HR system of record changes"),
    ("Azure DevOps", "gate release pipelines on Nimbus health checks before promoting a build"),
    ("Google Workspace", "provision and deprovision users from your Google directory"),
    ("OneLogin", "provision and deprovision Nimbus users from an alternate identity provider"),
    ("Intercom", "surface a customer's recent usage history to support agents inline"),
    ("Airtable", "mirror workspace metadata into a shared operations base"),
    ("Metabase", "build lightweight internal dashboards on top of exported usage data"),
    ("dbt", "model exported Nimbus tables alongside the rest of your warehouse"),
    ("Fivetran", "manage the Snowflake and BigQuery syncs through a single pipeline tool"),
    ("Retool", "build internal admin tools against the Nimbus API without custom scaffolding"),
    ("Opsgenie", "route critical alerts as an alternative to the PagerDuty integration"),
    ("Freshdesk", "give support agents visibility into a customer's usage history"),
    ("Coupa", "route Enterprise invoices through existing procurement approval workflows"),
    ("Docusign", "route Enterprise contract amendments through existing e-signature workflows"),
    ("Miro", "embed a live snapshot of architecture diagrams referencing Nimbus resources"),
    ("Linear", "open and track Linear issues from detected anomalies as an alternative to Jira"),
    ("Asana", "mirror onboarding checklist tasks into a shared Asana project"),
    ("Grafana", "build custom infrastructure dashboards on top of Nimbus metrics"),
    ("New Relic", "forward application performance data for unified monitoring"),
    ("Sentry", "correlate error spikes with recent Nimbus deployments"),
    ("LaunchDarkly", "gate Nimbus configuration rollouts behind feature flags"),
    ("Vault", "manage Nimbus API key rotation using existing secrets infrastructure"),
    ("CloudFlare", "route traffic through an existing CDN and WAF configuration"),
    ("Postman", "import a maintained collection covering the full v3 API surface"),
    ("Excel", "export scheduled reports directly into a workbook via the Data Export add-on"),
    ("PowerBI", "build executive reporting dashboards on top of exported usage data"),
    ("Chef", "manage on-prem agent configuration alongside existing infrastructure-as-code"),
    ("Puppet", "manage on-prem agent configuration as an alternative to the Chef integration"),
    ("Ansible", "automate Nimbus workspace provisioning as part of a broader deployment playbook"),
    ("Kubernetes", "run the Nimbus on-prem agent as a first-class workload via the official Helm chart"),
    ("Jenkins", "gate release pipelines on Nimbus health checks as an alternative to CircleCI"),
    ("Bitbucket", "mirror the GitHub integration's deploy and rollback triggers for Bitbucket Pipelines"),
    ("Trello", "mirror onboarding checklist tasks into a shared Trello board"),
    ("Monday.com", "mirror onboarding checklist tasks into a shared Monday.com board"),
    ("SAP", "sync invoice line items into SAP as an alternative to the NetSuite integration"),
]

def integrations_section():
    paras = ["## Integrations\n\nNimbus connects to the tools your team already uses. Below is the current catalog of first-party integrations; custom integrations can be built against our public API."]
    for name, desc in INTEGRATIONS:
        paras.append(
            f"### {name} Integration\n\nThe {name} integration lets you {desc}. "
            f"Setup takes about five minutes: authorize {name} from the Integrations "
            f"tab, pick which workspace or project should receive data, and choose a "
            f"sync frequency. Most customers leave the default hourly sync in place, "
            f"but real-time streaming is available on Growth and Enterprise plans. "
            f"If you run into trouble, our support team can usually diagnose "
            f"{name} sync issues within one business day."
        )
    return "\n\n".join(paras)

DOC_PARTS = [
"""# Nimbus Data Platform — Product Documentation

Nimbus Data Platform helps engineering and data teams manage infrastructure, billing, and access control from a single console. This document covers everything a new admin needs to know: pricing, onboarding, integrations, security, and support.""",

"""## Pricing

We offer three tiers designed for teams of every size.

- Starter: $100/month, billed monthly at $100/month, or $1,000/year if billed annually.
- Growth: $500/month, billed monthly at $500/month, or $5,000/year if billed annually.
- Enterprise: $2,000/month, billed monthly at $2,000/month, or $20,000/year if billed annually.

All tiers include unlimited seats and a 99.9% uptime SLA. Overage charges apply beyond the included quota, billed at $0.01 per extra API call. Enterprise customers can negotiate custom overage rates with their account manager.""",

"""## Legacy API (v1)

The original v1 API was launched in 2015 and used XML payloads over SOAP. It has been deprecated since 2020 and will be fully shut down at the end of this year. We strongly recommend migrating to the v3 REST API, which offers better performance and JSON support. Documentation for the legacy v1 API is still available on request, but we no longer add new features to it, and security patches are issued on a best-effort basis only.""",

"""## Getting Started

Signing up is quick. Just create an account, pick a plan, and invite your team. Most customers are up and running in under ten minutes. Our onboarding team is also happy to hop on a call if you want a guided walkthrough. We think you're gonna love how easy it is to get your infra sorted out. Once you're in, the first thing most teams do is connect their first data source and set up a workspace for each environment (dev, staging, prod).""",

"""## Onboarding Checklist

New workspaces should complete the following steps in their first week: invite at least one teammate, connect a data source, configure a billing contact, set up single sign-on if required by your security team, and review the default alerting thresholds. Teams that complete all five steps in week one see meaningfully higher long-term retention, so our onboarding specialists will proactively check in if any step is still outstanding after day five.""",

integrations_section(),

"""## Rate Limits

API requests are limited per workspace, not per user. Starter workspaces get 100 requests per minute, Growth workspaces get 1,000 requests per minute, and Enterprise workspaces get 10,000 requests per minute with the option to raise this further on request. Requests beyond the limit receive a 429 response with a Retry-After header. We recommend implementing exponential backoff in any client that calls the API on a schedule, since bursty traffic is the most common cause of rate limiting in practice.""",

"""## Webhooks

Nimbus can push events to a webhook endpoint you control: deployments, billing events, anomaly detections, and user management events (invites, removals, role changes) are all available as webhook topics. Payloads are signed with an HMAC secret so you can verify authenticity on your end. We retry failed webhook deliveries with exponential backoff for up to 24 hours before giving up and surfacing the failure in the console.

Webhook endpoints can be scoped to a subset of topics, which most teams use to avoid flooding a general-purpose channel with low-signal events. We also provide a built-in delivery log so you can replay any individual event without waiting for the next retry window, which is useful when a downstream consumer was briefly down for maintenance.""",

"""## API Authentication

All API requests are authenticated with a workspace-scoped API key, passed as a bearer token. Keys can be scoped to read-only or read-write access, and Enterprise customers can further scope a key to specific projects. We recommend rotating API keys at least every 90 days and immediately revoking any key that may have been exposed in a log file or client-side bundle. OAuth2 is also available for integrations that act on behalf of an individual user rather than the workspace as a whole.""",

"""## SDKs and Client Libraries

Official SDKs are available for Python, Node.js, Go, and Java, with community-maintained libraries for Ruby and PHP. Each SDK wraps the REST API with typed request and response objects, handles retries and rate-limit backoff automatically, and is versioned independently from the API itself so upgrading your SDK never silently changes API behavior. Source for all official SDKs is public, and we accept community pull requests for bug fixes and minor feature additions.""",

"""## Environments

Most teams create at least three projects per workspace: development, staging, and production. Development projects have relaxed rate limits and shorter data retention, since their data is typically synthetic or short-lived. Production projects default to the full retention and audit logging described elsewhere in this document. It's possible to promote configuration from one environment to another using the Terraform integration, which avoids the drift that comes from configuring each environment by hand in the console.""",

"""## Data Export

Workspace owners can export all workspace data at any time in CSV or Parquet format, either through the console or via the API. Exports include usage events, audit logs, and billing history, but not raw payload bodies for privacy reasons unless explicitly requested and approved by our security team. Enterprise customers can additionally schedule recurring exports to a customer-owned storage bucket, which many use to satisfy internal data retention policies that exceed our default retention windows.""",

"""## Enterprise Add-ons

Enterprise customers can add several optional capabilities on top of the base plan: a dedicated infrastructure tenant, custom data retention windows, a private Slack Connect channel with our engineering team, and a quarterly architecture review with a Nimbus solutions engineer. These add-ons are priced separately from the base Enterprise tier and are typically negotiated as part of the annual contract renewal.""",

"""## Single Sign-On

Growth and Enterprise plans support SAML-based single sign-on with any identity provider that implements the standard, including Okta, OneLogin, Azure AD, and Google Workspace. Once SSO is enabled, workspace owners can optionally require it for all members, which disables password-based login entirely for that workspace. SCIM provisioning is available as an add-on for Enterprise customers who want member invites and removals to be driven entirely from their identity provider rather than the Nimbus console.""",

"""## Two-Factor Authentication

Members who sign in with a password can enable two-factor authentication using any TOTP-compatible authenticator app. Workspace owners on Growth and Enterprise plans can require two-factor authentication for all members who are not using SSO. Recovery codes are generated at enrollment and should be stored somewhere other than the device running the authenticator app, since losing both will require a manual identity verification with support to regain access.""",

"""## IP Allowlisting

Enterprise customers can restrict API and console access to a list of approved IP ranges. This is commonly combined with SSO so that even a compromised session token is unusable outside the corporate network. Allowlist changes take effect within five minutes and are recorded in the audit log like any other configuration change.""",

"""## Sandbox Mode

Every workspace includes a sandbox project that mirrors production configuration but uses synthetic data and does not count against your plan's rate limits or billed API usage. Sandbox mode is the recommended place to test integration changes, webhook consumers, and SDK upgrades before rolling them out to production. Data in the sandbox project is reset automatically every 30 days.""",

"""## Custom Domains

Enterprise customers can serve the Nimbus console and API under their own domain instead of the default nimbus.example domain. Setting this up requires adding a CNAME record and a short verification step; our infrastructure team provisions and renews the TLS certificate automatically so there's nothing to maintain on your end after the initial setup.""",

"""## Status Page and Incident History

Our public status page reports uptime for the API, console, and each regional data residency option separately, along with a 90-day incident history. Workspace owners can subscribe to status updates by email, SMS, or webhook. Post-incident reviews for any incident affecting more than a small number of customers are published within five business days of resolution.""",

"""## API Versioning Policy

The current API version is v3. We commit to at least 12 months of notice before deprecating a version, and we maintain parallel support for the outgoing and incoming versions throughout that window so integrations can migrate on their own schedule. Breaking changes are never introduced within a version; they always ship as a new version instead, which is part of why the v1 to v3 migration has taken several years to fully complete across our customer base.""",

"""## Regional Availability

Nimbus infrastructure currently runs in the United States (primary), the European Union, and the United Kingdom, with an Asia-Pacific region in private beta for select Enterprise customers. Choosing a region affects both data residency and typical API latency; customers with users concentrated in a particular region generally see the best latency by hosting their primary workspace there, even if data residency isn't otherwise a requirement.""",

"""## Localization

The Nimbus console is available in English, Spanish, French, German, and Japanese, with the display language following each member's browser locale by default. API responses, error messages, and webhook payloads are always in English regardless of console language, since most integrations consuming them are automated rather than read by a human directly.""",

"""## Mobile SDKs

In addition to our server-side SDKs, we offer mobile SDKs for iOS and Android that let client applications report usage events directly, with automatic batching and offline queuing so events aren't lost when a device loses connectivity. Mobile SDK events are rate-limited more generously than server-side API calls, since a single workspace may have thousands of concurrent mobile clients.""",

"""## Metric Definitions

Active Workspace: a workspace with at least one API call or console login in the trailing 30 days.
Included Quota: the number of API calls a plan includes before overage billing applies, reset at the start of each billing cycle.
Anomaly Score: an internal 0-100 score reflecting how unusual a given usage pattern is relative to that workspace's own baseline, not relative to other customers.
Sync Lag: the delay between an event occurring in a source system and it becoming visible in Nimbus, reported per integration in the admin console.""",

"""## Audit Log Reference

Every audit log entry includes an actor (the member or API key that made the change), an action, the affected resource, a timestamp, and the source IP address. Audit logs are immutable and cannot be edited or deleted by anyone, including workspace owners; Enterprise customers can stream audit logs to their own SIEM in near real time via the Splunk integration or a generic webhook.""",

"""## Terms of Service Summary

This section is a plain-language summary and does not replace the full Terms of Service available on our website. Nimbus does not use customer data to train any models. Customers own their data and can export or delete it at any time, subject to the backup retention windows described elsewhere in this document. Either party may terminate a monthly plan at any time; annual plans are subject to the notice period specified in the signed order form.""",

"""## Admin Console

The admin console is where workspace owners manage billing, members, and security settings. From here you can view a full audit log of every configuration change, going back 12 months on Growth and Enterprise plans (90 days on Starter). The audit log includes who made the change, what changed, and the IP address the request came from, which is often the first thing our support team asks for when investigating an unexpected configuration change.

The console also surfaces a real-time usage dashboard scoped to the current billing cycle, broken down by project and integration, so admins can see well before the monthly invoice arrives whether a workspace is trending toward an overage. Most Enterprise customers configure a Slack alert at 75% of included quota specifically so finance isn't surprised by the number on the invoice.""",

"""## Known Limitations

A handful of things are worth knowing up front. Workspace region cannot be changed without a guided migration, as noted in Data Residency. Custom roles are Enterprise-only; Growth workspaces are limited to the four built-in roles. Webhook payloads are capped at 256KB; larger payloads are truncated with a pointer to the full event via the API. Sandbox projects cannot receive live webhook deliveries, only synthetic test events triggered manually from the console.""",

"""## Case Studies

A mid-market fintech company migrated from a self-hosted alternative to Nimbus in three weeks, citing the audit log and SOC 2 certification as the deciding factors for their compliance team. A logistics company on the Enterprise plan uses custom roles to give warehouse operations staff read-only access to a single project while keeping engineering's write access scoped to their own. A media company running mostly on the Starter plan uses the Zapier integration as their primary automation layer instead of building against the API directly, which they've found sufficient for their relatively low request volume.""",

"""## Support SLA Detail

Response time SLAs describe the time to first response, not time to resolution; complex issues may take longer to fully resolve even after an engineer has responded. Critical issues are defined as anything causing a full outage of a customer's ability to read or write data; degraded performance and non-blocking bugs are handled as standard priority even on Enterprise plans. SLA credits are available for Enterprise customers if a critical issue's first response exceeds the committed one-hour window, and are applied automatically to the next invoice without requiring a support ticket to claim them.""",

"""## Roles and Permissions

Nimbus supports four built-in roles: Owner, Admin, Member, and Viewer. Owners can manage billing and delete the workspace; Admins can manage members and integrations but not billing; Members can read and write data within their assigned projects; Viewers have read-only access. Enterprise customers can additionally define custom roles with fine-grained permissions scoped to individual resources, which is common for organizations that need to separate production access from staging access at the role level rather than relying on separate workspaces.""",

"""## Backups and Disaster Recovery

All customer data is backed up nightly, with backups retained for 30 days on Starter and Growth plans and 90 days on Enterprise. Backups are stored in a separate region from primary storage and are tested with a quarterly restore drill. In the event of a regional outage, Nimbus can fail over to a secondary region within our documented RTO of four hours and RPO of fifteen minutes; Enterprise customers can request a tighter RTO/RPO agreement as part of a custom contract.""",

"""## Data Residency

By default, workspace data is stored in the United States. Customers on Growth and Enterprise plans can choose to store data in the European Union or United Kingdom instead, which is common for customers with GDPR or UK data protection obligations. Changing data residency after a workspace has been created requires a guided migration performed by our infrastructure team and typically takes one to two weeks depending on data volume.""",

"""## Security

Nimbus Data Platform is SOC 2 Type II certified. All data is encrypted at rest and in transit. We run regular third-party penetration tests and publish a summary of results annually. Access to production systems is limited to a small on-call rotation and requires hardware security keys. We also maintain a private bug bounty program for security researchers who want to report vulnerabilities responsibly.""",

"""## Compliance

In addition to SOC 2 Type II, Nimbus maintains ISO 27001 certification and undergoes an annual HIPAA readiness assessment for healthcare customers who sign a Business Associate Agreement. Compliance reports and certificates are available to Enterprise customers under NDA through the trust portal linked from the admin console.""",

"""## Billing FAQ

Q: How much does the Starter plan cost?
A: The Starter plan is $100/month, with no long-term contract required.

Q: Can I switch plans mid-cycle?
A: Yes, upgrades take effect immediately and are prorated; downgrades take effect at the start of the next billing cycle.

Q: Do you offer annual billing discounts?
A: Yes, annual billing is discounted relative to paying monthly, as shown in the Pricing section above.

Q: What happens if I exceed my plan's included API quota?
A: You'll be billed for overage at the per-call rate listed in the Pricing section; we'll also email you a warning at 80% and 100% of your included quota so there are no surprises.

Q: Do you offer nonprofit or startup discounts?
A: Yes, approved nonprofits and startups under two years old can apply for a 20% discount on Growth and Enterprise plans through our website.

Q: What payment methods do you accept?
A: We accept all major credit cards and, for Enterprise customers, ACH transfer or wire against a quarterly or annual invoice.

Q: Can I get a refund if I cancel mid-cycle?
A: Monthly plans are not refunded for partial months; annual plans canceled within the first 30 days are refunded in full.

Q: Is there a free trial?
A: Yes, all new workspaces start with a 14-day trial of Growth features before falling back to the Starter plan automatically.""",

"""## Migration Guide

Moving from another platform to Nimbus generally takes two to four weeks depending on data volume and the number of integrations in use. Our migration team will help you map your existing schema, run a shadow sync to validate data parity, and schedule a cutover window with minimal downtime. Most customers run their old platform and Nimbus in parallel for one to two weeks before fully cutting over, which gives everyone confidence that nothing was lost in translation.

Enterprise migrations additionally get a dedicated migration engineer for the full duration of the project, a shared Slack Connect channel for day-to-day questions, and a formal cutover runbook reviewed jointly by both teams before the cutover window is scheduled. We've found that migrations with a written runbook have meaningfully fewer cutover-day surprises than ones planned informally over email.""",

"""## Support

Starter customers get email support with a 48-hour response time. Growth customers get email and chat support with a 4-hour response time. Enterprise customers get a dedicated Slack channel and a named support engineer, with a 1-hour response time for critical issues. All plans include access to our public status page and community forum.

Support is available in English at all tiers, with Spanish and Japanese available during business hours in the relevant region for Growth and Enterprise customers. Community forum questions are typically answered by other customers or our developer relations team within a day, and don't count against any plan's support response SLA since the forum is best-effort rather than a formal support channel.""",

"""## Changelog Highlights

Over the past year we've shipped webhook support for anomaly detection events, custom roles for Enterprise customers, EU and UK data residency options, a redesigned admin console audit log, and expanded rate limits for Growth plan customers. We also launched the Terraform provider, added Parquet as an export format, introduced scoped API keys, and rebuilt the onboarding checklist based on customer feedback. We publish a full changelog on our public site and send a monthly digest email to workspace owners who opt in.""",

"""## Glossary

Workspace: the top-level container for a customer's data, members, and billing.
Project: a logical grouping of resources within a workspace, often mapped to an environment like dev, staging, or prod.
Anomaly: an automatically detected deviation from expected usage patterns, surfaced in the admin console and optionally via webhook.
Overage: usage beyond a plan's included quota, billed at the per-unit rate for that plan.
RTO: recovery time objective, the maximum acceptable time to restore service after an outage.
RPO: recovery point objective, the maximum acceptable amount of data loss measured in time.
Scoped API key: an API key restricted to read-only access, a specific project, or both.
Shadow sync: a read-only trial replication run during migration to validate data parity before cutover.
Trust portal: the Enterprise-only page where compliance certificates and reports are shared under NDA.
Cutover: the point during a migration when a customer's production traffic switches from their old platform to Nimbus.""",
]

def main():
    source = "\n\n".join(DOC_PARTS)
    word_count = len(source.split())
    changes = [
        "Update the pricing section to reflect a 10% increase across all tiers",
        "Remove the paragraph about the legacy API",
        "Make the tone throughout more formal",
        "Add a one-sentence note at the end of the Security section mentioning our SOC 2 Type II certification was last renewed in March 2027",
    ]
    payload = {"sourceDocument": source, "changes": changes}
    out_path = os.path.join(os.path.dirname(__file__), "sample4_large.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {out_path} ({word_count} words, {len(source)} chars)")

if __name__ == "__main__":
    main()
