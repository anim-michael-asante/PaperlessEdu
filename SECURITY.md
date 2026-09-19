# Security Policy

PaperlessEdu handles sensitive school, financial, and minors' data. Security
issues should be reported privately and should not be disclosed publicly until
the issue has been assessed and a fix or mitigation is available.

## Supported Versions

The project is currently under active development and has no released versions.
Security support applies to the latest development version on the default
branch. Once releases begin, this table will be updated with the supported
release window.

| Version                       | Supported    |
| ----------------------------- | ------------ |
| Latest development version    | Yes          |
| Older or unreleased snapshots | No guarantee |

## Reporting a Vulnerability

Use GitHub's private **Security advisories** workflow for this repository when
it is enabled. Include:

- A concise description of the issue and its impact.
- The affected commit, version, URL, or component.
- Reproduction steps or a minimal proof of concept.
- Any suggested mitigation.

Do not include real student records, credentials, API keys, or other personal
data in a report. Use synthetic data when demonstrating the issue.

If private security advisories are unavailable, contact the repository
maintainer through a private GitHub channel and request a security contact.
Do not open a public issue for an unpatched vulnerability.

## Response Process

We will acknowledge a valid report as soon as practical, confirm the affected
scope, and coordinate a fix or mitigation. Timing depends on severity and
whether a safe fix can be prepared without exposing affected users.

After remediation, the project may publish a security advisory describing the
impact, affected versions, fixed version, and any required upgrade steps.

## Development Security Requirements

- Never commit secrets, credentials, `.env` files, local databases, or student
  data.
- Keep Django and third-party dependencies updated and review security alerts.
- Keep `DEBUG = False` and configure explicit `ALLOWED_HOSTS` in deployment.
- Use HTTPS, secure session and CSRF cookies, and restrictive security headers
  in production.
- Enforce authentication, authorization, and object-level access checks for
  every student, grade, attendance, finance, and document operation.
- Validate uploads by type and size, store them safely, and do not trust client
  filenames or extensions.
- Do not log passwords, tokens, payment details, or unnecessary personal data.
