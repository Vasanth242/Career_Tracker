# jobs/tasks.py  ← Rename this file to jobs/fetcher.py (optional) or keep as is
import feedparser
import requests
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .models import Job
from accounts.models import Profile

# Your exact job boards
JOB_SOURCES = [
    {"name": "Relocate.me", "url": "https://relocate.me/jobs/rss"},
    {"name": "StepStone.de", "url": "https://www.stepstone.de/rss/jobs.rss?wt=1&what=python+django+robot+framework&where=deutschland"},
    {"name": "Arbeitnow", "url": "https://www.arbeitnow.com/api/job-board-api"},
    {"name": "MyCareersFuture", "url": "https://api.mycareersfuture.gov.sg/v2/jobs?limit=30&sortBy=new_posting_date&search=python+django+automation+testing"},
    {"name": "JobsInFinland", "url": "https://jobsinfinland.fi/feed/"},
    {"name": "IamExpat NL", "url": "https://www.iamexpat.nl/rss/career/jobs-netherlands.xml"},
    {"name": "WorkHere NZ", "url": "https://workhere.co.nz/jobs/rss"},
]

def extract_keywords(text, profile_skills):
    if not text:
        return []
    text_lower = text.lower()
    return [skill for skill in profile_skills if skill and skill.lower() in text_lower]

# THIS IS NOW A NORMAL FUNCTION — NO CELERY!
def fetch_jobs():
    profiles = Profile.objects.select_related('user').all()
    total_new = 0

    for profile in profiles:
        user = profile.user
        skills = [s.strip() for s in (profile.key_skills or []) if s.strip()]
        roles = [r.strip().lower() for r in (profile.preferred_roles or []) if r.strip()]
        countries = [c.strip().lower() for c in (profile.target_countries or []) if c.strip()]

        new_jobs = []

        for source in JOB_SOURCES:
            try:
                print(f"Fetching from {source['name']}...")
                if "mycareersfuture" in source["url"]:
                    resp = requests.get(source["url"], timeout=15)
                    if resp.status_code == 200:
                        data = resp.json().get("results", [])
                        for item in data:
                            title = item.get("title", "No title")
                            company = item.get("company", {}).get("name", "Unknown")
                            url = item.get("applyUrl") or item.get("jobUrl", "#")
                            desc = (item.get("description", "") + " " + item.get("requirements", "")).strip()

                            if any(role in title.lower() for role in roles) or any(skill.lower() in desc.lower() for skill in skills):
                                if not Job.objects.filter(user=user, url=url).exists():
                                    job = Job.objects.create(
                                        user=user,
                                        title=title,
                                        company=company,
                                        location="Singapore",
                                        source="MyCareersFuture",
                                        url=url,
                                        description=desc[:1000],
                                        tags=extract_keywords(desc, skills),
                                        status='new'
                                    )
                                    new_jobs.append(job)
                                    total_new += 1

                elif "arbeitnow" in source["url"]:
                    resp = requests.get(source["url"], timeout=15)
                    if resp.status_code == 200:
                        for item in resp.json().get("data", []):
                            title = item.get("title", "")
                            if not any(role in title.lower() for role in roles):
                                continue
                            if not Job.objects.filter(user=user, url=item["url"]).exists():
                                job = Job.objects.create(
                                    user=user,
                                    title=title,
                                    company=item.get("company_name", "Unknown"),
                                    location="Germany",
                                    source="Arbeitnow",
                                    url=item["url"],
                                    description=" ".join(item.get("tags", [])),
                                    tags=item.get("tags", []),
                                    status='new'
                                )
                                new_jobs.append(job)
                                total_new += 1

                else:
                    # RSS Feeds
                    feed = feedparser.parse(source["url"])
                    for entry in feed.entries[:20]:
                        title = getattr(entry, "title", "No title")
                        url = getattr(entry, "link", "#")
                        desc = getattr(entry, "description", "") or getattr(entry, "summary", "")
                        company = getattr(entry, "author", "Unknown")

                        if any(role in title.lower() for role in roles) or any(skill.lower() in desc.lower() for skill in skills):
                            if not Job.objects.filter(user=user, url=url).exists():
                                location = next((c for c in countries if c in desc.lower() or c in title.lower()), "International")
                                job = Job.objects.create(
                                    user=user,
                                    title=title,
                                    company=company,
                                    location=location.title(),
                                    source=source["name"],
                                    url=url,
                                    description=desc[:1000],
                                    tags=extract_keywords(desc + title, skills),
                                    status='new'
                                )
                                new_jobs.append(job)
                                total_new += 1

            except Exception as e:
                print(f"Error with {source['name']}: {e}")

        # Send email
        if new_jobs and profile.email_notifications and user.email:
            subject = f"New Jobs Alert! ({len(new_jobs)} found)"
            message = f"Hi {user.get_full_name() or user.username},\n\nWe found {len(new_jobs)} new jobs for you:\n\n"
            for j in new_jobs[:10]:
                message += f"• {j.title}\n  {j.company} — {j.location}\n  → {j.url}\n\n"
            message += "Login: http://127.0.0.1:8000/jobs/\n\nGood luck!\n— Career Tracker"

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=True)

    print(f"Job fetch complete! Added {total_new} new jobs.")