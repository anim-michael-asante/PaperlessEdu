# PaperlessEdu Documentation

## Overview

PaperlessEdu is a Django-based school management system for individual schools.
It replaces paper-heavy processes such as attendance, grading, report cards,
fees, and school communication with one organized system.

This is a single-school deployment model. A school contacts PaperlessEdu, we
visit or work with the school to configure its deployment, and the school's
team runs its own system. This is not a shared multi-tenant SaaS product.

The public website is a landing page for schools and visitors. Visitors do not
log in from the landing page. The primary conversion action is contacting
PaperlessEdu to discuss setup.

## Tech Stack

- Django 6.0.6
- Python 3.13
- Django templates, CSS, and vanilla HTML for the public landing page
- SQLite for local development
- PostgreSQL planned for production
- `requirements.txt` pins Django

## Current Project Structure

```text
PaperlessEdu/
├── documentation.md
├── implementation-plan.md
├── README.md
├── SECURITY.md
├── LICENSE.md
├── requirements.txt
└── paperlessedu/
    ├── manage.py
    ├── paperlessedu/       # Django project configuration
    ├── accounts/           # authentication and roles
    ├── students/           # student records
    ├── academics/          # classes and academic structure
    ├── grading/            # grades and report cards
    ├── attendance/         # attendance records
    ├── finance/            # fees, invoices, and payments
    ├── notifications/      # SMS, email, and announcements
    ├── library/            # library module
    └── core/               # shared utilities and public website
```

All nine Django apps are registered in `paperlessedu/settings.py`. Each app is
currently a valid generated Django scaffold with its migrations package.

## Build Phase Log

### Completed

- Created the Django project and nine domain apps.
- Registered all local apps in `INSTALLED_APPS`.
- Applied Django's initial built-in migrations.
- Added the repository `.gitignore` for Python, Django, virtual environment,
  database, secret, test, and editor artifacts.
- Added `SECURITY.md` with reporting guidance and project security rules.
- Added `LICENSE.md` using the MIT License.
- Added a public welcome route at `/` through the `core` app.
- Built the first landing-page screen with:
  - lavender, cream, and white grid visual system
  - DM Serif Display and Manrope typography
  - responsive navigation and hero content
  - feature cards for attendance, overview, and communication
  - setup-focused contact calls to action
  - dynamic viewport-height hero behavior
  - reduced-motion and keyboard focus support
- Removed visitor login from the public landing page. School setup is the
  intended next action.
- Verified `python manage.py check` passes.
- Integrated official brand logo assets and favicon suite:
  - Extracted clean transparent brand emblem and master icon (`paperlessedu-icon.png`).
  - Generated multi-size `favicon.ico` (16x16, 32x32, 48x48), `favicon-32x32.png`, `favicon-16x16.png`, and `apple-touch-icon.png` (180x180).
  - Added `site.webmanifest` for PWA and mobile shortcut icon specifications.
  - Generated standard 1200x630 `og-image.png` with brand identity and feature highlights for WhatsApp, iMessage, Twitter/X, and social media link sharing previews.
  - Configured Open Graph (`og:*`) and Twitter Card (`twitter:*`) meta tags in `<head>`.
  - Added official brand emblem to the navigation wordmark, official logo to the contact section, and a clean branded site footer.
  - Standardized icons to Lucide Icons CDN with zero emojis.
- Added automated unit tests in `core/tests.py` covering route response, favicon links, Open Graph metadata, and brand logo presence (all tests passing).

### Not Yet Built

- Custom user model and role-based access control.
- School, student, academic, grade, attendance, finance, and notification
  models.
- Admin workflows and authenticated school staff screens.
- Report card PDF generation.
- Contact form processing or a real sales inbox.
- PostgreSQL, Celery, Redis, SMS integration, PWA support, and deployment
  configuration.

## Public User Flow

1. Visitor opens `/`.
2. Visitor reads what PaperlessEdu manages for a school.
3. Visitor selects `Contact us`, `Talk to us about setup`, or the contact CTA.
4. PaperlessEdu arranges a setup conversation with the school.
5. A school-specific deployment is configured for the school team.
6. Staff users will later log in through the private application workflow, not
   through the public landing page.

## Design Decisions

- The welcome page follows the supplied visual reference: soft lavender and
  cream gradients, a fine grid, serif display typography, compact sans-serif
  navigation, dark rounded buttons, and floating cards.
- The hero is `100dvh` so it fits the browser viewport, including mobile browser
  viewport changes.
- The first screen has one clear purpose: explain the service and generate a
  school setup conversation.
- The landing page uses no real API, authentication, database data, or student
  information.
- The public contact link currently uses `mailto:hello@paperlessedu.com` as a
  placeholder until the final business contact address is confirmed.

## Security Notes

- Do not place student, parent, financial, or staff data in the public landing
  page.
- Keep secrets in environment variables and never commit `.env` files.
- The current development settings are not production-ready: `DEBUG` must be
  disabled, `SECRET_KEY` must come from an environment variable, and
  `ALLOWED_HOSTS`, HTTPS, secure cookies, and security headers must be set for
  deployment.
- A custom user model should be created before domain migrations are built.
- Authorization must be enforced for every school staff operation once the
  private management system is implemented.

## Next Recommended Steps

1. Confirm the real business contact email and replace the placeholder mailto.
2. Create the custom `accounts.User` model before any domain migrations.
3. Define the core school, academic year, term, class, student, and enrollment
   models.
4. Add focused model and permission tests.
5. Build the staff/admin workflow after the public landing page is approved.
6. Add report card generation as the first product milestone.

## Local Development

From the repository root:

```powershell
.venv\Scripts\Activate.ps1
cd paperlessedu
python manage.py check
python manage.py runserver
```

The public landing page is available at `http://127.0.0.1:8000/`.
