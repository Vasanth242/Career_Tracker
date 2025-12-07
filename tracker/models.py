# tracker/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Goal(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    CATEGORY_CHOICES = [
        ('course', 'Course'),
        ('certification', 'Certification'),
        ('project', 'Project'),
        ('job_applications', 'Job Applications'),
        ('skill', 'Skill Building'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    start_date = models.DateField(null=True, blank=True)
    target_completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('goal_detail', args=[self.pk])

    @property
    def progress(self):
        """Calculate progress based on completed tasks"""
        total_tasks = self.task_set.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.task_set.filter(status='completed').count()
        return int((completed_tasks / total_tasks) * 100)


class Task(models.Model):
    STATUS_CHOICES = Goal.STATUS_CHOICES

    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='task_set')
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.description[:50]


class Course(models.Model):
    STATUS_CHOICES = Goal.STATUS_CHOICES

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=100, help_text="e.g., Udemy, Coursera, YouTube")
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    certificate_url = models.URLField(blank=True, null=True, help_text="Link to certificate")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.platform}"

    def get_absolute_url(self):
        return reverse('courses')


class Project(models.Model):
    STATUS_CHOICES = Goal.STATUS_CHOICES
    TYPE_CHOICES = [
        ('full_stack', 'Full Stack'),
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('automation', 'Automation'),
        ('dashboard', 'Dashboard'),
        ('mobile', 'Mobile App'),
        ('api', 'API Development'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='other')
    description = models.TextField()
    tech_stack = models.TextField(
        help_text="Comma-separated list, e.g., Python, Django, React, PostgreSQL"
    )
    github_url = models.URLField(blank=True, null=True)
    live_url = models.URLField(blank=True, null=True, verbose_name="Live Demo URL")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects')

    def tech_stack_list(self):
        """Return list of tech items for template use"""
        if not self.tech_stack:
            return []
        return [tech.strip() for tech in self.tech_stack.split(',') if tech.strip()]