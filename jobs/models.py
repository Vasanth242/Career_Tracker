from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class JobSource(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    job_search_url = models.URLField()

    def __str__(self):
        return f"{self.label} ({self.country})"

class Job(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('ignored', 'Ignored'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')  # User-specific jobs
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    source = models.CharField(max_length=100)
    url = models.URLField()
    description = models.TextField()
    date_posted = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    tags = JSONField(default=list)  # e.g., ['Python', 'Django']

    def __str__(self):
        return self.title

    @property
    def relevance(self):
        # Simple matching logic
        profile = self.user.profile
        score = 0
        if self.location in profile.target_countries:
            score += 1
        for role in profile.preferred_roles:
            if role.lower() in self.title.lower():
                score += 1
        matching_skills = set(profile.key_skills) & set(self.tags)
        score += len(matching_skills)
        if score >= 3:
            return 'Highly Relevant'
        elif score >= 1:
            return 'Relevant'
        return 'Low Relevance'