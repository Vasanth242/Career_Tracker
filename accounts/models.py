# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    current_role = models.CharField(max_length=100, default='Software Engineer')
    target_countries = JSONField(default=list)  # e.g., ['Singapore', 'Germany', 'Finland', 'Switzerland']
    preferred_roles = JSONField(default=list)  # e.g., ['Software Engineer', 'Backend Developer']
    key_skills = JSONField(default=list)  # e.g., ['Python', 'Django', 'SQL']
    email_notifications = models.BooleanField(default=True)
    reminder_time = models.TimeField(default='21:00:00')  # 9 PM

    def __str__(self):
        return self.name