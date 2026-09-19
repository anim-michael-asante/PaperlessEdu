# PaperlessEdu — Implementation Plan

**Built by Aerixis** | Django-based paperless school management system (Web App + PWA)

---

## 1. Project Overview

PaperlessEdu replaces a school's paper-based processes — enrollment, attendance, grading, report cards, fee receipts, and parent communication — with a secure, auditable digital system. It is built as both a portfolio piece (demonstrating full-stack + AppSec engineering) and a sellable product, delivered per-contract to individual schools (single-tenant deployments).

**Build order:**
1. Core data model (students, grading, terms)
2. Report card PDF generation (first milestone/demo)
3. Attendance
4. Fees
5. SMS notifications layered on top

---

## 2. System Architecture

### 2.1 High-Level Architecture
- **Pattern:** Monolithic Django app (single-tenant per school) — simplest to build, secure, and deploy per contract
- **Frontend:** Django templates + HTMX/vanilla JS for interactivity, styled with Tailwind or Bootstrap
- **PWA layer:** `django-pwa` for manifest.json + service worker (installability, basic asset caching)
- **Backend:** Django (ORM, views, forms, auth)
- **Database:** PostgreSQL (production), SQLite (local dev only)
- **Task queue:** Celery + Redis — for SMS sending, PDF generation, scheduled reminders (async, so requests don't block)
- **File storage:** Local filesystem for MVP; migrate to S3-compatible storage (e.g. Backblaze B2, DigitalOcean Spaces) once handling real student documents/photos at scale

### 2.2 Module Boundaries (Django apps)
```
paperlessedu/
├── accounts/        # auth, roles, RBAC
├── students/        # student info system
├── academics/       # courses, classes, timetable
├── grading/         # gradebook, exams, report cards
├── attendance/      # daily/period attendance
├── finance/         # fees, invoices, receipts
├── notifications/   # SMS, email, announcements
├── library/          # optional module
├── core/            # school settings, shared utilities, audit log
```

### 2.3 Data Flow Example (Fee Payment → SMS)
```
Admin records payment → Payment model saved → Django signal fires
  → Celery task queued → SMS provider API called → MessageLog updated
```
Async by design — a slow SMS provider should never block the admin's UI.

---

## 3. Security Architecture

Security is a differentiator here, not an afterthought — worth treating as a first-class design pillar given the AppSec angle.

### 3.1 Authentication & Authorization
- Django's built-in auth, extended with a custom `User` model from day one (never retrofit this later)
- **RBAC**: role field (Admin, Teacher, Student, Parent) + Django Groups/Permissions for granular control
- Enforce **object-level permissions** where needed (e.g., a teacher can only edit grades for their own classes) — `django-guardian` is worth evaluating here
- Strong password policy via Django's validators; consider enforcing MFA for Admin accounts specifically (highest-value target)
- Session security: `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, short session timeout for admin roles

### 3.2 Data Protection
- **Encryption in transit:** HTTPS everywhere (required anyway for PWA service workers)
- **Encryption at rest:** database-level encryption for sensitive fields (fee/financial data at minimum)
- **Data isolation:** since each school is a separate deployment, isolation is inherent — but still enforce strict query scoping (no cross-school queries possible by design)
- **Minors' data:** treat student data as sensitive by default — least-privilege access, no unnecessary data collection, clear data retention policy per contract

### 3.3 Application Security (OWASP-aligned)
- CSRF protection (Django default — verify it's never disabled)
- SQL injection: rely on Django ORM, avoid raw queries; if unavoidable, use parameterized queries only
- XSS: Django template auto-escaping — verify no `|safe` misuse, sanitize any rich-text input (e.g., announcements)
- File upload validation: restrict file types/size, scan or sandbox uploaded documents (assignment files, ID photos)
- Rate limiting on login and password reset (`django-ratelimit` or similar) — prevents brute force
- Security headers: `django-csp`, `X-Frame-Options`, `X-Content-Type-Options`, HSTS

### 3.4 Audit Logging
- Dedicated `AuditLog` model: who changed what, when, old/new values — especially for grades, fees, and user permission changes
- This becomes a genuine sales point: "every grade change is traceable"

### 3.5 Secrets & Config
- Environment variables for all secrets (`django-environ`), never committed
- Separate settings per environment (dev/staging/production)
- SMS provider credentials stored encrypted, configurable per-school deployment

---

## 4. System Design (Data Model Highlights)

### Core entities
- `School` (settings: name, logo, term dates, grading scale)
- `User` → `AdminProfile` / `TeacherProfile` / `StudentProfile` / `ParentProfile`
- `AcademicYear` → `Term`
- `Class` / `Section` → `Enrollment` (student ↔ class ↔ term)
- `Subject` → `ClassSubject` (subject taught in a class by a teacher)
- `Grade` (student, subject, term, score) → aggregated into `ReportCard`
- `AttendanceRecord` (student, class, date, status)
- `Invoice` → `Payment` → triggers `MessageLog` entry
- `Announcement`, `MessageTemplate`, `MessageLog`
- `AuditLog` (generic: actor, action, model, object_id, timestamp, diff)

Design principle: keep `School` settings as configurable data so the same codebase serves every contract with minimal code changes — just data/config per deployment.

---

## 5. API Design

Even in a template-first build, an API layer is worth including:

- **Django REST Framework** for a thin API surface — enables future mobile app, third-party integrations, or a richer PWA offline sync later without a rewrite
- Versioned endpoints (`/api/v1/...`)
- Token or session auth depending on client (session for the web app itself, token/JWT if a separate client ever consumes it)
- Rate-limit and permission-check every endpoint the same as the web views — don't let the API become the weaker-guarded backdoor
- Priority endpoints: attendance marking, grade entry, payment recording (the ones most likely to benefit from async/offline submission later)

---

## 6. Performance & Speed

- **Database:** index foreign keys and frequently filtered fields (student ID, class, term, date); use `select_related`/`prefetch_related` to avoid N+1 queries in gradebook/report card views
- **Caching:** Redis for frequently-read, rarely-changed data (school settings, class lists, timetable)
- **PDF generation:** run as a Celery task, not inline in the request — report cards for a whole class should never block the browser
- **PWA caching:** service worker caches static assets and the app shell for fast repeat loads
- **Pagination:** enforce on all list views (student lists, attendance history) — never return unbounded querysets
- **Query budget mindset:** treat teacher-facing pages (attendance, gradebook) as the ones that most need to feel instant — this is where "paperless" wins or loses against the paper register

---

## 7. Reliability

- **Automated backups:** daily PostgreSQL backups, tested restore process (a backup you've never restored isn't a backup)
- **Error tracking:** Sentry or similar — catch production errors before a client reports them
- **Health checks:** basic uptime monitoring per deployment
- **Graceful degradation:** if SMS provider is down, queue and retry rather than failing silently — surface delivery status to admin
- **Idempotency:** payment recording and SMS sending should be safe to retry without duplicate charges/messages

---

## 8. Development Workflow

- **Version control:** Git, feature-branch workflow, meaningful commit messages
- **Environments:** local (SQLite/Docker), staging, production — never test against a live school's data
- **Testing:**
  - Unit tests for models and business logic (grade calculation, GPA, invoice totals)
  - Integration tests for critical flows (enrollment → attendance → report card; payment → SMS)
  - Security-focused tests: permission checks per role, CSRF, auth boundary tests
- **CI:** GitHub Actions — run tests + linting (`flake8`/`ruff`, `black`) on every push
- **Code review:** even solo, use PRs to yourself for anything touching auth/permissions/finance — forces a second pass

---

## 9. Deployment & DevOps (added)

- **Hosting:** decide per contract — you-managed (recurring revenue, recurring support) vs. school-managed. A platform like Railway, Render, or a VPS (DigitalOcean) with Docker Compose (Django + Postgres + Redis + Celery worker) is a reasonable default
- **Containerization:** Docker from the start — makes per-school deployment repeatable and consistent
- **CI/CD:** auto-deploy to staging on merge; manual promotion to each school's production instance
- **Domain/SSL:** subdomain or custom domain per school, HTTPS via Let's Encrypt/Caddy

---

## 10. Monitoring & Observability (added)

- Application logs centralized (even simple — e.g. Sentry + basic log aggregation)
- Track SMS delivery success/failure rates — a silently failing notification system defeats the whole pitch
- Admin-facing dashboard for system health per school (optional but strong differentiator)

---

## 11. Data Privacy & Compliance (added)

- Since this handles minors' data, treat this seriously even without a specific legal mandate in Ghana yet:
  - Data minimization — collect only what's needed
  - Clear data retention/deletion policy per contract (what happens to data if a school stops using the system)
  - Parent/guardian consent considerations for SMS communication
  - Document your security practices — this becomes both a compliance safety net and a sales asset

---

## 12. Documentation (added)

- README per repo, matching your ShopNow pattern (features, setup, security notes, screenshots/demo video)
- Admin setup guide (per-school onboarding checklist — settings, first admin account, SMS provider config)
- API docs if DRF is included (`drf-spectacular` for auto-generated OpenAPI docs)

---

## 13. Milestone Recap

| Phase | Deliverable |
|---|---|
| 1 | Scope decision finalized, core data model built |
| 2 | Report card PDF generation working — first demo |
| 3 | Attendance module |
| 4 | Fees/finance module |
| 5 | SMS notifications layered on top (fee confirmations, PTA invites) |
| 6 | Security hardening pass + audit logging polish |
| 7 | Deployment pipeline + first real/demo school instance |
