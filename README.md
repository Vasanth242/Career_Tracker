# Career Tracker

A Django-based web application for tracking career preparation progress and receiving job notifications for roles abroad.

## Setup and Installation

1. **Prerequisites**
   - Python 3.8+
   - Virtual environment (recommended): `python -m venv venv` then `source venv/bin/activate` (Unix) or `venv\Scripts\activate` (Windows)

2. **Install Dependencies**


3. **Project Setup**
- Create the project directory and place the files as per the structure.
- Run migrations: `python manage.py makemigrations` then `python manage.py migrate`
- Create a superuser: `python manage.py createsuperuser` (for admin access)
- Run the server: `python manage.py runserver`

4. **Configuration**
- In `settings.py`, ensure `DEBUG = True` for local dev.
- Target countries, roles, skills are editable in the profile/settings page.
- Job sources can be added/edited in the settings page.
- To fetch mock jobs: Use the admin panel or run `python manage.py fetch_jobs` (adds sample data).

5. **Features**
- User registration/login/logout.
- Dashboard with summaries.
- Track goals, tasks, courses, projects.
- Job listing with mock fetch, relevance matching, status updates.
- Settings to customize profile, countries, roles, skills, job sources.
- Basic notifications (badge for new jobs).

6. **Job Fetching**
- Currently uses mock data. Run `python manage.py fetch_jobs` to populate sample jobs.
- In future, extend the command to scrape or use APIs (respect ToS).

7. **Deployment Notes**
- For production (e.g., Render/Railway), set `DEBUG = False`, use PostgreSQL if needed, add env vars for SECRET_KEY.

## How to Configure
- After login, go to Settings to update profile, countries, roles, skills, job sources.
- Skills are comma-separated (e.g., "Python, Django, SQL").
- Job sources: Add entries like label="LinkedIn Singapore", url="https://www.linkedin.com/jobs/search/?location=Singapore".

## Code Quality
- Apps: core (shared), accounts, tracker, jobs.
- Comments and docstrings provided.
- Uses Bootstrap for simple styling (include CDN in base.html).

career_tracker/
├── manage.py
├── career_tracker/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
├── accounts/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│       ├── registration.html
│       ├── login.html
│       ├── profile.html
├── tracker/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│       ├── dashboard.html
│       ├── goals.html
│       ├── tasks.html
│       ├── courses.html
│       ├── projects.html
├── jobs/
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── management/
│   │   ├── __init__.py
│   │   ├── commands/
│   │       ├── __init__.py
│   │       ├── fetch_jobs.py
│   ├── templates/
│       ├── jobs.html
│       ├── settings.html  # Shared with accounts for job sources
├── templates/
│   ├── base.html
│   ├── navbar.html
├── static/
│   └── css/
│       └── styles.css  # Optional custom CSS
├── db.sqlite3  # Generated on migrate

## New Features
- Periodic job fetching: Run `python manage.py fetch_jobs` manually or via Celery scheduler.
- Email notifications for new relevant jobs.
- Daily 9 PM reminder email to study/update progress (links to dashboard).
- Configure in Settings: Enable emails, set reminder time.

## Celery Setup
1. Install: `pip install celery redis django-celery-beat django-celery-results`
2. Run Redis: `redis-server` (download from https://redis.io/)
3. Workers: `celery -A career_tracker worker -l info`
4. Scheduler: `celery -A career_tracker beat -l info`
5. Email: Set EMAIL_* in settings.py (e.g., Gmail SMTP).

Schedules:
- Jobs fetch: Every 6 hours.
- Daily reminder: 9 PM UTC (adjust timezone in settings).