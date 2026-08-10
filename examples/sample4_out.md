# Nimbus Data Platform — Product Documentation

Nimbus Data Platform assists engineering and data teams in managing infrastructure, billing, and access control from a single console. This document encompasses all essential information a new administrator needs: pricing, onboarding, integrations, security, and support.

## Pricing

We offer three tiers designed to accommodate teams of all sizes.

- Starter: $110/month, billed monthly at $110/month, or $1,100/year if billed annually.
- Growth: $550/month, billed monthly at $550/month, or $5,500/year if billed annually.
- Enterprise: $2,200/month, billed monthly at $2,200/month, or $22,000/year if billed annually.

All tiers include unlimited seats and a 99.9% uptime SLA. Overage charges apply beyond the included quota, billed at $0.01 per additional API call. Enterprise customers may negotiate custom overage rates with their account manager.

## Legacy API (v1)

## Getting Started

Signing up is straightforward. Simply create an account, select a plan, and invite your team. Most customers are operational in under ten minutes. Our onboarding team is also available for a guided walkthrough if desired. We believe you will appreciate the ease with which you can organize your infrastructure. Once onboarded, the initial step for most teams is to connect their first data source and establish a workspace for each environment (development, staging, production).

## Onboarding Checklist

New workspaces should complete the following steps within their first week: invite at least one teammate, connect a data source, configure a billing contact, set up single sign-on if required by your security team, and review the default alerting thresholds. Teams that complete all five steps in the first week experience significantly higher long-term retention, so our onboarding specialists will proactively check in if any step remains outstanding after five days.

## Integrations

Nimbus integrates with the tools your team already utilizes. Below is the current catalog of first-party integrations; custom integrations can be developed against our public API.

### Salesforce Integration

The Salesforce integration lets you sync leads, contacts, and opportunities in real time. Setup takes about five minutes: authorize Salesforce from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Salesforce sync issues within one business day.

### Slack Integration

The Slack integration lets you post deployment and billing alerts directly into any channel. Setup takes about five minutes: authorize Slack from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Slack sync issues within one business day.

### Zapier Integration

The Zapier integration lets you connect Nimbus to over five thousand other apps without writing code. Setup takes about five minutes: authorize Zapier from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Zapier sync issues within one business day.

### HubSpot Integration

The HubSpot integration lets you keep marketing and product usage data in lockstep. Setup takes about five minutes: authorize HubSpot from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose HubSpot sync issues within one business day.

### Jira Integration

The Jira integration lets you automatically open tickets when an anomaly is detected. Setup takes about five minutes: authorize Jira from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Jira sync issues within one business day.

### GitHub Integration

The GitHub integration lets you trigger deploys and roll back releases from pull request status. Setup takes about five minutes: authorize GitHub from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose GitHub sync issues within one business day.

### Segment Integration

The Segment integration lets you forward event streams into your existing analytics warehouse. Setup takes about five minutes: authorize Segment from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Segment sync issues within one business day.

### Snowflake Integration

The Snowflake integration lets you replicate raw usage tables on an hourly schedule. Setup takes about five minutes: authorize Snowflake from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Snowflake sync issues within one business day.

### BigQuery Integration

The BigQuery integration lets you run federated queries against your Nimbus data without exporting it. Setup takes about five minutes: authorize BigQuery from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose BigQuery sync issues within one business day.

### Looker Integration

The Looker integration lets you build dashboards on top of live Nimbus metrics. Setup takes about five minutes: authorize Looker from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Looker sync issues within one business day.

### Datadog Integration

The Datadog integration lets you forward infrastructure metrics and traces for unified monitoring. Setup takes about five minutes: authorize Datadog from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Datadog sync issues within one business day.

### PagerDuty Integration

The PagerDuty integration lets you route critical alerts to the right on-call engineer automatically. Setup takes about five minutes: authorize PagerDuty from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose PagerDuty sync issues within one business day.

### Okta Integration

The Okta integration lets you provision and deprovision Nimbus users automatically from your identity provider. Setup takes about five minutes: authorize Okta from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Okta sync issues within one business day.

### Microsoft Teams Integration

The Microsoft Teams integration lets you post deployment and billing alerts into a Teams channel. Setup takes about five minutes: authorize Microsoft Teams from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Microsoft Teams sync issues within one business day.

### Notion Integration

The Notion integration lets you publish a live snapshot of key usage metrics into a shared workspace page. Setup takes about five minutes: authorize Notion from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Notion sync issues within one business day.

### Tableau Integration

The Tableau integration lets you connect Nimbus datasets directly to existing Tableau dashboards. Setup takes about five minutes: authorize Tableau from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Tableau sync issues within one business day.

### AWS S3 Integration

The AWS S3 integration lets you archive raw event data to a customer-owned bucket on a nightly schedule. Setup takes about five minutes: authorize AWS S3 from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose AWS S3 sync issues within one business day.

### Google Cloud Storage Integration

The Google Cloud Storage integration lets you mirror exported reports into GCS for downstream processing. Setup takes about five minutes: authorize Google Cloud Storage from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Google Cloud Storage sync issues within one business day.

### Terraform Integration

The Terraform integration lets you manage workspaces, roles, and integrations as code. Setup takes about five minutes: authorize Terraform from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Terraform sync issues within one business day.

### Okta Workflows Integration

The Okta Workflows integration lets you chain Nimbus events into broader identity automation pipelines. Setup takes about five minutes: authorize Okta Workflows from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Okta Workflows sync issues within one business day.

### Amplitude Integration

The Amplitude integration lets you cross-reference product usage events with Nimbus infrastructure metrics. Setup takes about five minutes: authorize Amplitude from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Amplitude sync issues within one business day.

### Mixpanel Integration

The Mixpanel integration lets you correlate user behavior with billing and overage events. Setup takes about five minutes: authorize Mixpanel from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Mixpanel sync issues within one business day.

### ServiceNow Integration

The ServiceNow integration lets you open and track incident tickets from detected anomalies. Setup takes about five minutes: authorize ServiceNow from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose ServiceNow sync issues within one business day.

### Confluence Integration

The Confluence integration lets you publish onboarding checklists and runbooks alongside live status. Setup takes about five minutes: authorize Confluence from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Confluence sync issues within one business day.

### Zendesk Integration

The Zendesk integration lets you give support agents read-only visibility into a customer's usage history. Setup takes about five minutes: authorize Zendesk from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Zendesk sync issues within one business day.

### Stripe Integration

The Stripe integration lets you reconcile Nimbus invoices against your existing billing records. Setup takes about five minutes: authorize Stripe from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Stripe sync issues within one business day.

### NetSuite Integration

The NetSuite integration lets you sync invoice line items into your ERP for finance reporting. Setup takes about five minutes: authorize NetSuite from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose NetSuite sync issues within one business day.

### CircleCI Integration

The CircleCI integration lets you gate deploys on Nimbus health checks before promoting a build. Setup takes about five minutes: authorize CircleCI from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose CircleCI sync issues within one business day.

### GitLab Integration

The GitLab integration lets you mirror the GitHub integration's deploy and rollback triggers. Setup takes about five minutes: authorize GitLab from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose GitLab sync issues within one business day.

### Splunk Integration

The Splunk integration lets you forward audit log events into an existing SIEM pipeline. Setup takes about five minutes: authorize Splunk from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Splunk sync issues within one business day.

### Workday Integration

The Workday integration lets you keep employee provisioning in sync with HR system of record changes. Setup takes about five minutes: authorize Workday from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Workday sync issues within one business day.

### Azure DevOps Integration

The Azure DevOps integration lets you gate release pipelines on Nimbus health checks before promoting a build. Setup takes about five minutes: authorize Azure DevOps from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Azure DevOps sync issues within one business day.

### Google Workspace Integration

The Google Workspace integration lets you provision and deprovision users from your Google directory. Setup takes about five minutes: authorize Google Workspace from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Google Workspace sync issues within one business day.

### OneLogin Integration

The OneLogin integration lets you provision and deprovision Nimbus users from an alternate identity provider. Setup takes about five minutes: authorize OneLogin from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose OneLogin sync issues within one business day.

### Intercom Integration

The Intercom integration lets you surface a customer's recent usage history to support agents inline. Setup takes about five minutes: authorize Intercom from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Intercom sync issues within one business day.

### Airtable Integration

The Airtable integration lets you mirror workspace metadata into a shared operations base. Setup takes about five minutes: authorize Airtable from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Airtable sync issues within one business day.

### Metabase Integration

The Metabase integration lets you build lightweight internal dashboards on top of exported usage data. Setup takes about five minutes: authorize Metabase from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Metabase sync issues within one business day.

### dbt Integration

The dbt integration lets you model exported Nimbus tables alongside the rest of your warehouse. Setup takes about five minutes: authorize dbt from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose dbt sync issues within one business day.

### Fivetran Integration

The Fivetran integration lets you manage the Snowflake and BigQuery syncs through a single pipeline tool. Setup takes about five minutes: authorize Fivetran from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Fivetran sync issues within one business day.

### Retool Integration

The Retool integration lets you build internal admin tools against the Nimbus API without custom scaffolding. Setup takes about five minutes: authorize Retool from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Retool sync issues within one business day.

### Opsgenie Integration

The Opsgenie integration lets you route critical alerts as an alternative to the PagerDuty integration. Setup takes about five minutes: authorize Opsgenie from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Opsgenie sync issues within one business day.

### Freshdesk Integration

The Freshdesk integration lets you give support agents visibility into a customer's usage history. Setup takes about five minutes: authorize Freshdesk from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Freshdesk sync issues within one business day.

### Coupa Integration

The Coupa integration lets you route Enterprise invoices through existing procurement approval workflows. Setup takes about five minutes: authorize Coupa from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Coupa sync issues within one business day.

### Docusign Integration

The Docusign integration lets you route Enterprise contract amendments through existing e-signature workflows. Setup takes about five minutes: authorize Docusign from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Docusign sync issues within one business day.

### Miro Integration

The Miro integration lets you embed a live snapshot of architecture diagrams referencing Nimbus resources. Setup takes about five minutes: authorize Miro from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Miro sync issues within one business day.

### Linear Integration

The Linear integration lets you open and track Linear issues from detected anomalies as an alternative to Jira. Setup takes about five minutes: authorize Linear from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Linear sync issues within one business day.

### Asana Integration

The Asana integration lets you mirror onboarding checklist tasks into a shared Asana project. Setup takes about five minutes: authorize Asana from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Asana sync issues within one business day.

### Grafana Integration

The Grafana integration lets you build custom infrastructure dashboards on top of Nimbus metrics. Setup takes about five minutes: authorize Grafana from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Grafana sync issues within one business day.

### New Relic Integration

The New Relic integration lets you forward application performance data for unified monitoring. Setup takes about five minutes: authorize New Relic from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose New Relic sync issues within one business day.

### Sentry Integration

The Sentry integration lets you correlate error spikes with recent Nimbus deployments. Setup takes about five minutes: authorize Sentry from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Sentry sync issues within one business day.

### LaunchDarkly Integration

The LaunchDarkly integration lets you gate Nimbus configuration rollouts behind feature flags. Setup takes about five minutes: authorize LaunchDarkly from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose LaunchDarkly sync issues within one business day.

### Vault Integration

The Vault integration lets you manage Nimbus API key rotation using existing secrets infrastructure. Setup takes about five minutes: authorize Vault from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Vault sync issues within one business day.

### CloudFlare Integration

The CloudFlare integration lets you route traffic through an existing CDN and WAF configuration. Setup takes about five minutes: authorize CloudFlare from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose CloudFlare sync issues within one business day.

### Postman Integration

The Postman integration lets you import a maintained collection covering the full v3 API surface. Setup takes about five minutes: authorize Postman from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Postman sync issues within one business day.

### Excel Integration

The Excel integration lets you export scheduled reports directly into a workbook via the Data Export add-on. Setup takes about five minutes: authorize Excel from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Excel sync issues within one business day.

### PowerBI Integration

The PowerBI integration lets you build executive reporting dashboards on top of exported usage data. Setup takes about five minutes: authorize PowerBI from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose PowerBI sync issues within one business day.

### Chef Integration

The Chef integration lets you manage on-prem agent configuration alongside existing infrastructure-as-code. Setup takes about five minutes: authorize Chef from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Chef sync issues within one business day.

### Puppet Integration

The Puppet integration lets you manage on-prem agent configuration as an alternative to the Chef integration. Setup takes about five minutes: authorize Puppet from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Puppet sync issues within one business day.

### Ansible Integration

The Ansible integration lets you automate Nimbus workspace provisioning as part of a broader deployment playbook. Setup takes about five minutes: authorize Ansible from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Ansible sync issues within one business day.

### Kubernetes Integration

The Kubernetes integration lets you run the Nimbus on-prem agent as a first-class workload via the official Helm chart. Setup takes about five minutes: authorize Kubernetes from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Kubernetes sync issues within one business day.

### Jenkins Integration

The Jenkins integration lets you gate release pipelines on Nimbus health checks as an alternative to CircleCI. Setup takes about five minutes: authorize Jenkins from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Jenkins sync issues within one business day.

### Bitbucket Integration

The Bitbucket integration lets you mirror the GitHub integration's deploy and rollback triggers for Bitbucket Pipelines. Setup takes about five minutes: authorize Bitbucket from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Bitbucket sync issues within one business day.

### Trello Integration

The Trello integration lets you mirror onboarding checklist tasks into a shared Trello board. Setup takes about five minutes: authorize Trello from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Trello sync issues within one business day.

### Monday.com Integration

The Monday.com integration lets you mirror onboarding checklist tasks into a shared Monday.com board. Setup takes about five minutes: authorize Monday.com from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose Monday.com sync issues within one business day.

### SAP Integration

The SAP integration lets you sync invoice line items into SAP as an alternative to the NetSuite integration. Setup takes about five minutes: authorize SAP from the Integrations tab, pick which workspace or project should receive data, and choose a sync frequency. Most customers leave the default hourly sync in place, but real-time streaming is available on Growth and Enterprise plans. If you run into trouble, our support team can usually diagnose SAP sync issues within one business day.

## Rate Limits

API requests are limited per workspace, not per user. Starter workspaces get 100 requests per minute, Growth workspaces get 1,000 requests per minute, and Enterprise workspaces get 10,000 requests per minute with the option to raise this further on request. Requests beyond the limit receive a 429 response with a Retry-After header. We recommend implementing exponential backoff in any client that calls the API on a schedule, since bursty traffic is the most common cause of rate limiting in practice.

## Webhooks

Nimbus can push events to a webhook endpoint you control: deployments, billing events, anomaly detections, and user management events (invites, removals, role changes) are all available as webhook topics. Payloads are signed with an HMAC secret so you can verify authenticity on your end. We retry failed webhook deliveries with exponential backoff for up to 24 hours before giving up and surfacing the failure in the console.

Webhook endpoints can be scoped to a subset of topics, which most teams use to avoid flooding a general-purpose channel with low-signal events. We also provide a built-in delivery log so you can replay any individual event without waiting for the next retry window, which is useful when a downstream consumer was briefly down for maintenance.

## API Authentication

All API requests are authenticated with a workspace-scoped API key, passed as a bearer token. Keys can be scoped to read-only or read-write access, and Enterprise customers can further scope a key to specific projects. We recommend rotating API keys at least every 90 days and immediately revoking any key that may have been exposed in a log file or client-side bundle. OAuth2 is also available for integrations that act on behalf of an individual user rather than the workspace as a whole.

## SDKs and Client Libraries

Official SDKs are available for Python, Node.js, Go, and Java, with community-maintained libraries for Ruby and PHP. Each SDK wraps the REST API with typed request and response objects, handles retries and rate-limit backoff automatically, and is versioned independently from the API itself so upgrading your SDK never silently changes API behavior. Source for all official SDKs is public, and we accept community pull requests for bug fixes and minor feature additions.

## Environments

Most teams create at least three projects per workspace: development, staging, and production. Development projects have relaxed rate limits and shorter data retention, since their data is typically synthetic or short-lived. Production projects default to the full retention and audit logging described elsewhere in this document. It's possible to promote configuration from one environment to another using the Terraform integration, which avoids the drift that comes from configuring each environment by hand in the console.

## Data Export

Workspace owners can export all workspace data at any time in CSV or Parquet format, either through the console or via the API. Exports include usage events, audit logs, and billing history, but not raw payload bodies for privacy reasons unless explicitly requested and approved by our security team. Enterprise customers can additionally schedule recurring exports to a customer-owned storage bucket, which many use to satisfy internal data retention policies that exceed our default retention windows.

## Enterprise Add-ons

Enterprise customers can add several optional capabilities on top of the base plan: a dedicated infrastructure tenant, custom data retention windows, a private Slack Connect channel with our engineering team, and a quarterly architecture review with a Nimbus solutions engineer. These add-ons are priced separately from the base Enterprise tier and are typically negotiated as part of the annual contract renewal.

## Single Sign-On

Growth and Enterprise plans support SAML-based single sign-on with any identity provider that implements the standard, including Okta, OneLogin, Azure AD, and Google Workspace. Once SSO is enabled, workspace owners can optionally require it for all members, which disables password-based login entirely for that workspace. SCIM provisioning is available as an add-on for Enterprise customers who want member invites and removals to be driven entirely from their identity provider rather than the Nimbus console.

## Two-Factor Authentication

Members who sign in with a password can enable two-factor authentication using any TOTP-compatible authenticator app. Workspace owners on Growth and Enterprise plans can require two-factor authentication for all members who are not using SSO. Recovery codes are generated at enrollment and should be stored somewhere other than the device running the authenticator app, since losing both will require a manual identity verification with support to regain access.

## IP Allowlisting

Enterprise customers can restrict API and console access to a list of approved IP ranges. This is commonly combined with SSO so that even a compromised session token is unusable outside the corporate network. Allowlist changes take effect within five minutes and are recorded in the audit log like any other configuration change.

## Sandbox Mode

Every workspace includes a sandbox project that mirrors production configuration but uses synthetic data and does not count against your plan's rate limits or billed API usage. Sandbox mode is the recommended place to test integration changes, webhook consumers, and SDK upgrades before rolling them out to production. Data in the sandbox project is reset automatically every 30 days.

## Custom Domains

Enterprise customers can serve the Nimbus console and API under their own domain instead of the default nimbus.example domain. Setting this up requires adding a CNAME record and a short verification step; our infrastructure team provisions and renews the TLS certificate automatically so there's nothing to maintain on your end after the initial setup.

## Status Page and Incident History

Our public status page reports uptime for the API, console, and each regional data residency option separately, along with a 90-day incident history. Workspace owners can subscribe to status updates by email, SMS, or webhook. Post-incident reviews for any incident affecting more than a small number of customers are published within five business days of resolution.

## API Versioning Policy

The current API version is v3. We commit to at least 12 months of notice before deprecating a version, and we maintain parallel support for the outgoing and incoming versions throughout that window so integrations can migrate on their own schedule. Breaking changes are never introduced within a version; they always ship as a new version instead, which is part of why the v1 to v3 migration has taken several years to fully complete across our customer base.

## Regional Availability

Nimbus infrastructure currently runs in the United States (primary), the European Union, and the United Kingdom, with an Asia-Pacific region in private beta for select Enterprise customers. Choosing a region affects both data residency and typical API latency; customers with users concentrated in a particular region generally see the best latency by hosting their primary workspace there, even if data residency isn't otherwise a requirement.

## Localization

The Nimbus console is available in English, Spanish, French, German, and Japanese, with the display language following each member's browser locale by default. API responses, error messages, and webhook payloads are always in English regardless of console language, since most integrations consuming them are automated rather than read by a human directly.

## Mobile SDKs

In addition to our server-side SDKs, we offer mobile SDKs for iOS and Android that let client applications report usage events directly, with automatic batching and offline queuing so events aren't lost when a device loses connectivity. Mobile SDK events are rate-limited more generously than server-side API calls, since a single workspace may have thousands of concurrent mobile clients.

## Metric Definitions

Active Workspace: a workspace with at least one API call or console login in the trailing 30 days.
Included Quota: the number of API calls a plan includes before overage billing applies, reset at the start of each billing cycle.
Anomaly Score: an internal 0-100 score reflecting how unusual a given usage pattern is relative to that workspace's own baseline, not relative to other customers.
Sync Lag: the delay between an event occurring in a source system and it becoming visible in Nimbus, reported per integration in the admin console.

## Audit Log Reference

Every audit log entry includes an actor (the member or API key that made the change), an action, the affected resource, a timestamp, and the source IP address. Audit logs are immutable and cannot be edited or deleted by anyone, including workspace owners; Enterprise customers can stream audit logs to their own SIEM in near real time via the Splunk integration or a generic webhook.

## Terms of Service Summary

This section is a plain-language summary and does not replace the full Terms of Service available on our website. Nimbus does not use customer data to train any models. Customers own their data and can export or delete it at any time, subject to the backup retention windows described elsewhere in this document. Either party may terminate a monthly plan at any time; annual plans are subject to the notice period specified in the signed order form.

## Admin Console

The admin console is where workspace owners manage billing, members, and security settings. From here you can view a full audit log of every configuration change, going back 12 months on Growth and Enterprise plans (90 days on Starter). The audit log includes who made the change, what changed, and the IP address the request came from, which is often the first thing our support team asks for when investigating an unexpected configuration change.

The console also surfaces a real-time usage dashboard scoped to the current billing cycle, broken down by project and integration, so admins can see well before the monthly invoice arrives whether a workspace is trending toward an overage. Most Enterprise customers configure a Slack alert at 75% of included quota specifically so finance isn't surprised by the number on the invoice.

## Known Limitations

A handful of things are worth knowing up front. Workspace region cannot be changed without a guided migration, as noted in Data Residency. Custom roles are Enterprise-only; Growth workspaces are limited to the four built-in roles. Webhook payloads are capped at 256KB; larger payloads are truncated with a pointer to the full event via the API. Sandbox projects cannot receive live webhook deliveries, only synthetic test events triggered manually from the console.

## Case Studies

A mid-market fintech company migrated from a self-hosted alternative to Nimbus in three weeks, citing the audit log and SOC 2 certification as the deciding factors for their compliance team. A logistics company on the Enterprise plan uses custom roles to give warehouse operations staff read-only access to a single project while keeping engineering's write access scoped to their own. A media company running mostly on the Starter plan uses the Zapier integration as their primary automation layer instead of building against the API directly, which they've found sufficient for their relatively low request volume.

## Support SLA Detail

Response time SLAs describe the time to first response, not time to resolution; complex issues may take longer to fully resolve even after an engineer has responded. Critical issues are defined as anything causing a full outage of a customer's ability to read or write data; degraded performance and non-blocking bugs are handled as standard priority even on Enterprise plans. SLA credits are available for Enterprise customers if a critical issue's first response exceeds the committed one-hour window, and are applied automatically to the next invoice without requiring a support ticket to claim them.

## Roles and Permissions

Nimbus supports four built-in roles: Owner, Admin, Member, and Viewer. Owners can manage billing and delete the workspace; Admins can manage members and integrations but not billing; Members can read and write data within their assigned projects; Viewers have read-only access. Enterprise customers can additionally define custom roles with fine-grained permissions scoped to individual resources, which is common for organizations that need to separate production access from staging access at the role level rather than relying on separate workspaces.

## Backups and Disaster Recovery

All customer data is backed up nightly, with backups retained for 30 days on Starter and Growth plans and 90 days on Enterprise. Backups are stored in a separate region from primary storage and are tested with a quarterly restore drill. In the event of a regional outage, Nimbus can fail over to a secondary region within our documented RTO of four hours and RPO of fifteen minutes; Enterprise customers can request a tighter RTO/RPO agreement as part of a custom contract.

## Data Residency

By default, workspace data is stored in the United States. Customers on Growth and Enterprise plans can choose to store data in the European Union or United Kingdom instead, which is common for customers with GDPR or UK data protection obligations. Changing data residency after a workspace has been created requires a guided migration performed by our infrastructure team and typically takes one to two weeks depending on data volume.

## Security

Nimbus Data Platform is SOC 2 Type II certified. All data is encrypted at rest and in transit. We run regular third-party penetration tests and publish a summary of results annually. Access to production systems is limited to a small on-call rotation and requires hardware security keys. We also maintain a private bug bounty program for security researchers who want to report vulnerabilities responsibly. Our SOC 2 Type II certification was last renewed in March 2027.

## Compliance

In addition to SOC 2 Type II, Nimbus maintains ISO 27001 certification and undergoes an annual HIPAA readiness assessment for healthcare customers who sign a Business Associate Agreement. Compliance reports and certificates are available to Enterprise customers under NDA through the trust portal linked from the admin console.

## Billing FAQ

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
A: Yes, all new workspaces start with a 14-day trial of Growth features before falling back to the Starter plan automatically.

## Migration Guide

Moving from another platform to Nimbus generally takes two to four weeks depending on data volume and the number of integrations in use. Our migration team will help you map your existing schema, run a shadow sync to validate data parity, and schedule a cutover window with minimal downtime. Most customers run their old platform and Nimbus in parallel for one to two weeks before fully cutting over, which gives everyone confidence that nothing was lost in translation.

Enterprise migrations additionally get a dedicated migration engineer for the full duration of the project, a shared Slack Connect channel for day-to-day questions, and a formal cutover runbook reviewed jointly by both teams before the cutover window is scheduled. We've found that migrations with a written runbook have meaningfully fewer cutover-day surprises than ones planned informally over email.

## Support

Starter customers get email support with a 48-hour response time. Growth customers get email and chat support with a 4-hour response time. Enterprise customers get a dedicated Slack channel and a named support engineer, with a 1-hour response time for critical issues. All plans include access to our public status page and community forum.

Support is available in English at all tiers, with Spanish and Japanese available during business hours in the relevant region for Growth and Enterprise customers. Community forum questions are typically answered by other customers or our developer relations team within a day, and don't count against any plan's support response SLA since the forum is best-effort rather than a formal support channel.

## Changelog Highlights

Over the past year we've shipped webhook support for anomaly detection events, custom roles for Enterprise customers, EU and UK data residency options, a redesigned admin console audit log, and expanded rate limits for Growth plan customers. We also launched the Terraform provider, added Parquet as an export format, introduced scoped API keys, and rebuilt the onboarding checklist based on customer feedback. We publish a full changelog on our public site and send a monthly digest email to workspace owners who opt in.

## Glossary

Workspace: the top-level container for a customer's data, members, and billing.
Project: a logical grouping of resources within a workspace, often mapped to an environment like dev, staging, or prod.
Anomaly: an automatically detected deviation from expected usage patterns, surfaced in the admin console and optionally via webhook.
Overage: usage beyond a plan's included quota, billed at the per-unit rate for that plan.
RTO: recovery time objective, the maximum acceptable time to restore service after an outage.
RPO: recovery point objective, the maximum acceptable amount of data loss measured in time.
Scoped API key: an API key restricted to read-only access, a specific project, or both.
Shadow sync: a read-only trial replication run during migration to validate data parity before cutover.
Trust portal: the Enterprise-only page where compliance certificates and reports are shared under NDA.
Cutover: the point during a migration when a customer's production traffic switches from their old platform to Nimbus.