# jobs/management/commands/fetch_jobs.py
from django.core.management.base import BaseCommand
from jobs.tasks import fetch_jobs  # ← This now works!

class Command(BaseCommand):
    help = 'Fetch real jobs from top international boards'

    def handle(self, *args, **kwargs):
        fetch_jobs()  # Runs immediately
        self.stdout.write(self.style.SUCCESS('Jobs fetched successfully! Check /jobs/ or Admin'))