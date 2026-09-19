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
- Expanded public landing page with requested sections and navigation tabs:
  - Navigation links: `How It Works`, `Services`, `What You'll Get`, `Testimonials`, `FAQ`, and `Contact us` button.
  - **Services Section** (`#services`): 6 core module cards (Student Records & Admissions, Daily & Period Attendance, Gradebook & Continuous Assessment, Instant Report Card PDF Engine, School Fees & Receipts, Automated Parent SMS & Alerts) with Lucide icons.
  - **What You'll Get Section** (`#what-you-get`): Replaced placeholder section with a 4-pillar value delivery grid detailing Private School Instance, On-Site Staff Training, Historical Record Digitization, and Continuous Support & Daily Backups.
  - **Testimonials Section** (`#testimonials`): High-trust review cards featuring Headmistress, Finance Administrator, and Academic Director quotes with rating stars and school badges.
  - **FAQ Section** (`#faq`): Accessible interactive accordion answering questions on setup, devices, offline resilience, custom report card crests, and data protection.
  - Enhanced mobile navigation: horizontal scrollable pill navigation ribbon ensuring accessible 44px touch targets on mobile viewports.
  - Added unit tests in `core/tests.py` covering all new navigation tabs, section anchors, and FAQ components (6 tests passing).
- Redesigned Contact Section based on visual reference image:
  - Floating dark luminous card (`.contact-card`) with deep midnight navy background (`#080c1f`).
  - Atmospheric right-side spotlight / light-bloom (`.contact-light-bloom`) blending soft white, icy cyan (`#e0f2fe`), bright teal (`#38bdf8`), and electric violet (`#6366f1`).
  - Category badge with PaperlessEdu emblem and tracked uppercase title: `SCHOOL ONBOARDING & SETUP`.
  - Bold, high-contrast title: *"Ready to transform your school?"* and slate subtitle.
  - Dual action buttons: primary solid white button (*"Talk to us about setup"*) and secondary translucent glass button (*"See how it works"*).
- Harmonized project colors and ambient grid across all background sections:
  - Enriched `#services`, `#what-you-get`, `#testimonials`, and `#faq` with subtle ambient radial tints and grid overlays matching the hero aesthetic.
- Aligned Contact Section with signature project colors:
  - Replaced harsh cyan/sky-blue lighting with the project's authentic palette: deep midnight plum/violet-ink card canvas (`#100b24` to `#251b47`) framed by soft lavender border highlights (`rgba(176, 168, 247, 0.32)`).
  - Atmospheric right-side spotlight bloom blending warm radiant cream (`#fff8e6`), luminous golden glow (`#ffe4a0`), soft lavender (`#b0a8f7`), and deep violet (`#7c3aed`) echoing the hero section.
  - Category pill badge in frosted lavender-violet (`rgba(176, 168, 247, 0.18)`).
- Designed and implemented modern multi-column footer matching the new visual reference:
  - 4-column responsive grid: Brand & Aerixis security badge, Platform Navigation, Core Modules, and Stay Updated newsletter signup.
  - Newsletter subscription pill with `@` prefix, email input, circular submit arrow button, and client-side accessible confirmation feedback.
  - Clean bottom bar with copyright notice, single-tenant security indicator, and Aerixis attribution.
  - Footer background styled with project color: deep midnight ink (`linear-gradient(180deg, #0d0a1d 0%, #080613 100%)`) with white headings, legible soft lavender text (`#b3afcb`), branded violet button (`#6358dc`), and high contrast passing WCAG AA.
- Hero Cards Visibility & Full Responsiveness:
  - Eliminated negative bottom positioning (`bottom: -54px`) and rigid clipping that previously hid the lower half of cards on laptop viewports.
  - Converted `.hero` to fluid `min-height: 100dvh; height: auto;` and `.card-stage` into a natural flex layout so cards remain 100% visible inside the viewport.
  - Interactive elevated fan arrangement on desktop with smooth hover lifts (`translateY(-6px)` and `-14px` on center card).
  - Full responsiveness across all breakpoints (desktop, tablet wrap, mobile vertical stack) ensuring all 3 cards with their avatars, icons, headlines, and status badges are visible to every visitor.
- Hero Section Alignment with Reference Image:
  - Aligned hero copy and card positioning to match reference image `media_1789849963677.png` exactly.
  - Positioned hero cards to peek gracefully from the bottom edge of the viewport with avatars (gold `A` + dark `T` on left card, sparkle icon on center card, dark `S` on right card), headlines, and status labels fully readable.
  - Applied interactive hover lifts on all cards.
- Mobile-First Responsiveness & Navigation Drawer:
  - Collapsed horizontal navigation into an accessible 44x44px touch-target hamburger toggle on mobile screens (`<= 860px`).
  - Added slide-in glassmorphism mobile navigation drawer (`.mobile-drawer`) with keyboard escape support and touch-friendly links (minimum 48px height).
  - Resolved floating badge collision on mobile viewports by safely hiding decorative badges on phone widths (`< 640px`) so typography is 100% unobstructed.
  - Lifted the hero cards on mobile view: elevated `.card-stage` to `240px` and lifted the center card to `bottom: 18px` (50px higher than before) while keeping desktop geometry intact. The cards fill the lower hero area, presenting the icons, avatars, and full headlines clearly.
  - Enhanced contact card contrast on mobile: softened radial light bloom to `opacity: 0.22`, protected all text with dark drop shadows, switched subtitle to `#ffffff`, and gave the secondary button a dark translucent glass backing (`rgba(16, 11, 36, 0.76)`) so all messages are 100% visible against the light transition.
  - Single-column responsive adaptations with fluid typography (`clamp()`) across 375px, 640px, 768px, and desktop viewports.
- GitHub Pages Static Compilation & Deployment Workflow:
  - Created [`export_static.py`](file:///g:/PaperlessEdu/export_static.py) to render the full Django template and package static assets into `_site/` with relative paths (`./static/core/...`), favicons, manifests, and `.nojekyll`.
  - Configured [`.github/workflows/static.yml`](file:///g:/PaperlessEdu/.github/workflows/static.yml) to checkout, install Python 3.12 dependencies, run `export_static.py _site`, and deploy directly via GitHub Actions Pages pipeline (`actions/deploy-pages@v4`).
- Project Color Multi-Column Footer:
  - Styled `.site-footer` with deep midnight ink background (`linear-gradient(180deg, #0d0a1d 0%, #080613 100%)`) and subtle lavender top border (`1px solid rgba(176, 168, 247, 0.18)`).
  - High-contrast typography: white headings/wordmark (`#ffffff`), soft lavender links and text (`#b3afcb`), and branded violet newsletter submit button (`#6358dc`).
- GitHub Pages Static Hosting Workflow:
  - Configured `.github/workflows/static.yml` to automatically build and deploy pure HTML and CSS to GitHub Pages on pushes to `main`.
  - Created `export_static.py` to compile the Django `welcome.html` view into a clean, self-contained static `_site` directory with relative links (`./`), static assets, favicon fallback, `.nojekyll`, and automatic Open Graph site URL resolution.
  - Added `_site/` to `.gitignore`.
- Expanded automated unit test suite in `core/tests.py` to 10 passing tests.

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
