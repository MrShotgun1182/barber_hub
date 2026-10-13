# CLAUDE.md — Rules and Developer Guide for Barber Hub Project

This file serves as the reference for rules, architecture, and conventions for the project. Read this file carefully before making any code modifications.

---

## 1. Project Overview

**Barber Hub** is a barbershop appointment booking system written in Persian:
- Customers log in via mobile number and OTP code, select a barber and service, and book an appointment.
- Barbers have a dedicated panel (today's appointments, services, working hours).
- Managers (MANAGER) have an administration panel (salon base services, today's appointments).

The project language is Persian: all `verbose_name` attributes, docstrings, error messages, and comments must remain in Persian.

---

## 2. Tech Stack

| Component | Technology |
| --- | --- |
| Backend | Django `>=5.0,<6.0` (Password validation disabled) |
| Database | PostgreSQL 15 |
| Asynchronous Tasks | Celery + Redis |
| SMS Provider | `melipayamak` package |
| Frontend | Tailwind CSS v4 (No config file; theme inside `input.css`) |
| Containerization | Docker + docker-compose |

---

## 3. Key Commands

```bash
# Run the complete stack (web + database + redis + celery)
docker compose up --build

# Generate and apply migrations
python manage.py makemigrations
python manage.py migrate

# Run the development server
python manage.py runserver

# Run Celery worker (for OTP SMS delivery)
celery -A core worker --loglevel=info

# Frontend: Compile Tailwind
cd frontend
npm run dev     # Watch mode → output to frontend/static/dist/output.css
npm run build   # Minified build for production

# Tests
python manage.py test
```

> **Note:** The final compiled CSS file is generated at `frontend/static/dist/output.css` and loaded into templates via `{% static 'dist/output.css' %}`. When adding new Tailwind classes, ensure the compiler is actively running.

---

## 4. Layered Architecture (Golden Rule)

Data flow is **strictly unidirectional**; no layer may invoke a higher layer:

```
Request → View → Action → Service → Model/DB
```

| Layer | Responsibility | Allowed Actions |
| --- | --- | --- |
| **View** | Receive request, parse input, render template or return JsonResponse | Call Actions only |
| **Action** | Service orchestration, validation, error handling, `transaction.atomic` | Call Services |
| **Service** | Pure database logic and business calculations | Interact with Model/ORM |
| **Model** | Database schema definition | — |

**Strict Rules:**
- Views **must not** call Services directly; only Actions.
- Views **must not** execute ORM queries directly.
- Business logic belongs in Actions and Services, not in Views or Models.
- Actions wrap multiple/atomic operations inside `transaction.atomic()` locally or within the calling service.

**Action Output Structure:** Actions typically return a `dict` and catch internal errors to prevent leakage to the view layer:

```python
# Standard Action Pattern
def SomeAction(...) -> dict:
    try:
        data = some_services.SomeService(...)
        return {'status': 'success', 'message': '...', **data}
    except ValueError as ve:
        return {'status': 'error', 'message': str(ve)}
    except Exception:
        return {'status': 'error', 'message': 'An error occurred. Please try again.'}
```

> Note: Certain authentication actions use `success` (boolean) and `error` keys (e.g., `BarberLoginAction`). However, the dominant pattern across API responses uses `status`/`message` keys. Align with sibling actions when creating a new action.

---

## 5. Naming Conventions

### File Naming — snake_case with Layer Suffix

| Layer | File Pattern | Function/Class Name Pattern |
| --- | --- | --- |
| Models | `[name]_model.py` | `[Name]Model` |
| Services | `[action]_[name]_service.py` | `[Action][Name]Service` |
| Actions | `[operation]_[name]_action.py` | `[Operation][Name]Action` |
| Views | `[name]_view.py` | `[Name]View` |
| Templates | `[name].html` | — |

**Examples:**
- `apps/booking/services/create_appointment_service.py` → Function `CreateAppointmentService`
- `apps/booking/actions/submit_booking_action.py` → Function `SubmitBookingAction`
- `apps/booking/views/select_datetime_view.py` → Function `SelectDatetimeView`

### Important Rules
- Functions in views/actions/services use **PascalCase** (not snake_case), even in views. Views are defined as **functions**, not classes (exception: `django.views.generic.TemplateView`, which is used only in `core/urls.py`).
- **All** directories under `views/`, `actions/`, `services/`, and `models/` contain an `__init__.py` file re-exporting symbols. Always import newly added files into the folder's `__init__.py`.
- In `admin_panel`, the action directory is capitalized: `Actions/` (historical inconsistency). Other apps use `actions/`. Follow the convention of the respective app.

### Import Pattern
The `apps/` directory is added to `sys.path` (in `core/settings.py`). Apps should be imported **without** the `apps.` prefix:

```python
from booking import services as booking_services
from barbers import models as barbers_models
from accounts import services as accounts_services
```

Using the alias pattern `import ... as ..._models` / `..._services` is standard practice to prevent name collisions. Continue following this style.

---

## 6. Project Structure

```
barber_hub/
├── core/                      # Root configuration: settings.py, urls.py, celery.py
├── apps/                      # Application modules (on sys.path)
│   ├── accounts/              # UserModel (AbstractUser + phone_number + role)
│   ├── barbers/               # BarberModel, BarberServiceModel, WorkingHoursModel
│   ├── customers/             # CustomerModel, CustomerHairstyleModel
│   ├── admin_panel/           # AdminPanelModel (Manager Profile) + Actions/ folder
│   ├── booking/               # AppointmentModel + Booking Wizard Flow
│   ├── salon_services/        # ServiceModel (Salon Base Services)
│   └── OTP/                   # OTPModel + Celery SMS task
├── frontend/                  # Tailwind + Global Templates + Static assets
│   ├── static/src/input.css   # Custom theme & color definitions (cream/sage)
│   ├── static/dist/output.css # Compiled Tailwind CSS output
│   └── templates/core/        # base.html, barber_base.html, admin_base.html, landing.html
└── manage.py
```

Each app under `apps/` follows this layout:
`models/`, `views/`, `actions/`, `services/`, `templates/<app>/`, `migrations/`, `admin.py`, `urls.py` (optional).

> **Apps without `urls.py`:** `OTP`, `customers`, `salon_services`. These are consumed internally or through other app views (e.g., `booking`). They are not directly registered in `core/urls.py`.

---

## 7. Domain Models & Key Relationships

- **`accounts.UserModel`** (Custom, `AUTH_USER_MODEL`): `AbstractUser` + `phone_number` (unique, 11 digits) + `role` in `{CUSTOMER, BARBER, MANAGER}`.
- **`barbers.BarberModel`**: `OneToOne` to User with `related_name='barber_profile'`.
- **`customers.CustomerModel`**: `OneToOne` to User with `related_name='customer_profile'`.
- **`admin_panel.AdminPanelModel`**: `OneToOne` to User with `related_name='manager_profile'`.
- **`salon_services.ServiceModel`**: Base service with `base_price` and `default_duration_minutes`.
- **`barbers.BarberServiceModel`**: Barber-specific service mapping (`unique_together=(barber, service)`) with `custom_price` and `custom_duration_minutes`. If null, base `ServiceModel` values apply.
- **`barbers.WorkingHoursModel`**: Weekly working schedules; `day_of_week` ranges from **0=Saturday to 6=Friday** (Python mapping: `(date.weekday() + 2) % 7`).
- **`booking.AppointmentModel`**: Booking slot with `ManyToMany` to `BarberServiceModel`, stored `total_price`/`total_duration_minutes`, and `status` in `{PENDING, CONFIRMED, COMPLETED, CANCELLED}`.

### Time Overlap Validation
Always use the standard overlap formula:
`max(start1, start2) < min(end1, end2)` → Overlaps exist.
Only appointments with `PENDING` and `CONFIRMED` statuses are considered during slot availability calculations.

---

## 8. Booking Wizard Flow

Divided into 4 isolated steps, each step having its **dedicated View/Action/Service**. State is maintained client-side in browser `sessionStorage`:

1. **OTP** — `SendOTPView`/`VerifyOTPView` → `SendOTPAction`/`VerifyOTPAction`
2. **Barber & Service Selection** — `SelectBarberAndServiceView` → `GetBookingOptionsAction`
3. **Date & Time Slot Selection** — `SelectDatetimeView` → `GetAvailableSlotsAction` → `CalculateAvailableSlotsService`
4. **Review & Final Submission** — `ReviewBookingView` → `SubmitBookingAction` → `CreateAppointmentService`

Routes are configured in `apps/booking/urls.py` with `app_name = 'booking'` and namespaced path names.

Detailed flow specifications are available in `appointment_std.md`.

---

## 9. OTP & SMS System

- 6-digit verification codes generated via `secrets` (`GenerateOTPCodeService`), saved in `OTPModel`, with a **2-minute expiration window**.
- SMS delivery handled **asynchronously** via Celery: `SendOTPSMSTask.delay(...)` → `SendSMSService` (`melipayamak` package).
- SMS provider credentials configured in `.env`: `MELIPAYAMAK_USERNAME`, `MELIPAYAMAK_PASSWORD`, `MELIPAYAMAK_FROM`.
- Code verification sets `is_used=True` atomically to prevent reuse.

---

## 10. URL Routing

- `core/urls.py`: `admin/` (Django admin), `accounts/`, `admin_panel/`, `barber/`, `booking/`, and `''` for landing page.
- Applications define `app_name`, and URLs are resolved via namespaces: `{% url 'barbers:barbers_dashboard' %}`.
- Views are registered directly as function endpoints: `path('...', views.SomeView, name='some_name')`.

---

## 11. Templates & Frontend

- Global templates reside in `frontend/templates/core/` (`DIRS` setting). App-specific templates reside in `apps/<app>/templates/<app>/`.
- Template inheritance extends from `core/base.html` (or `core/barber_base.html` / `core/admin_base.html` for dashboards).
- Default document language is `fa` with `dir="rtl"`.
- Tailwind v4: **No `tailwind.config.js` exists**. Classes are auto-scanned from templates, and custom themes are defined inside `frontend/static/src/input.css` using `@theme` (`cream-*` and `sage-*` palettes).
- Use brand colors via utility classes such as `bg-sage-500` or `text-cream-100`.

---

## 12. Authentication & Access Control

- Customer Login: Phone + OTP → `GetOrCreateUserByPhoneService` creates user with `CUSTOMER` role and executes `login()`.
- Barber Login: restricted to users with `role == 'BARBER'` and active profiles (`is_active=True`) via `BarberLoginAction`.
- Manager Login: requires `role == 'MANAGER'`, `is_staff`, or `is_superuser` via `AdminLoginAction`.
- Panel views are secured with `@login_required` and manual role checks. Always verify access controls when adding new view functions.

---

## 13. Known Technical Debt & Gotchas

Keep these points in mind when working on the codebase; **do not alter or refactor them unless explicitly requested**:

- `SECRET_KEY`, `DEBUG=True`, and `AUTH_PASSWORD_VALIDATORS = []` are hardcoded in `settings.py` for development mode. These require updating before production deployment.
- In `apps/OTP/`, both a `models/` package and a standalone `apps/OTP/models.py` file exist. The package takes precedence, making `models.py` dead code — make changes inside `models/OTP_model.py`.
- `apps/OTP/views.py` is a single file rather than a `views/` directory package and lacks a `urls.py`; it is invoked through the `booking` module.
- `SendSMSService` contains debug `print()` statements that output sensitive information.
- The `Actions/` folder in `admin_panel` uses uppercase naming, differing from other apps.
- AJAX/Fetch requests expecting JSON send an `x-requested-with: XMLHttpRequest` header or a `?format=json` query parameter (pattern seen in `SelectBarberAndServiceView`).

---

## 14. Feature Implementation Checklist

1. Model (if required) → `models/<name>_model.py` + register in `models/__init__.py` + run migrations.
2. Services → `services/<action>_<name>_service.py` + register in `services/__init__.py`.
3. Action → `actions/<operation>_<name>_action.py` + register in `actions/__init__.py`.
4. View → `views/<name>_view.py` + register in `views/__init__.py`.
5. Route → Register in the app's `urls.py` with an appropriate `name`.
6. Template (if required) → `templates/<app>/<name>.html`.
7. Ensure all error messages and `verbose_name` strings are written in Persian.

---

## 15. Project Skills

Project-specific skill configurations are stored under `.claude/skills/`:

- **`add-feature`** — Step-by-step checklist for adding new features (Model → Service → Action → View → Route → Template), reminding developers to export modules in `__init__.py` files and maintain Persian messaging.
- **`run-stack`** — Commands for launching the application stack (Docker or local + Celery + Tailwind) along with environment prerequisites.
- **`git-commit`** — Clean git commit workflow: explicit file staging (avoiding `git add .`), reviewing `git diff --staged`, adhering to Conventional Commits, and isolating unrelated changes.

---

## 16. Code Style Guidelines

- Single-line Persian docstrings for every major function explaining the layer's responsibility.
- Type annotations for all service and action parameters (`barber_id: int`, `barber_service_ids: list[int]`, `-> dict`).
- Numbered Persian comments (`# ۱. ...`, `# ۲. ...`) detailing steps inside longer function blocks.
- Variable and function names in English; user messages, strings, and labels in Persian.