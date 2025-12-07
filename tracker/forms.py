# tracker/forms.py
from django import forms
from .models import Goal, Task, Course, Project


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'category', 'start_date', 'target_completion_date', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., Master Python Automation',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none text-lg font-medium'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'start_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'},
                format='%Y-%m-%d'
            ),
            'target_completion_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'},
                format='%Y-%m-%d'
            ),
        }
        labels = {
            'title': 'Goal Title',
            'category': 'Category',
            'start_date': 'Start Date',
            'target_completion_date': 'Target Completion Date',
            'status': 'Current Status',
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description', 'due_date', 'status', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'e.g., Complete Robot Framework crash course',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none resize-none'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Additional notes, resources, challenges...',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none resize-none'
            }),
        }
        labels = {
            'description': 'Task Description',
            'due_date': 'Due Date (Optional)',
            'status': 'Status',
            'notes': 'Notes',
        }


class CourseForm(forms.ModelForm):
    # Make certificate optional
    certificate_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://certificate-link.com (optional)',
            'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
        })
    )

    class Meta:
        model = Course
        fields = ['name', 'platform', 'start_date', 'completion_date', 'status', 'certificate_url', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'e.g., Advanced Django Mastery',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none text-lg font-medium'
            }),
            'platform': forms.TextInput(attrs={
                'placeholder': 'e.g., Udemy, Coursera, YouTube',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'completion_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Key takeaways, projects built, skills learned...',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none resize-none'
            }),
        }
        labels = {
            'name': 'Course Name',
            'platform': 'Platform',
            'start_date': 'Start Date',
            'completion_date': 'Completion Date',
            'status': 'Status',
            'certificate_url': 'Certificate Link (Optional)',
            'notes': 'Notes / Achievements',
        }


class ProjectForm(forms.ModelForm):
    # Make URLs optional
    github_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://github.com/username/repo (optional)',
            'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
        })
    )
    live_url = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://yourapp.com (optional)',
            'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
        })
    )

    tech_stack = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, Django, React, PostgreSQL, Tailwind',
            'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
        }),
        help_text="Separate with commas"
    )

    class Meta:
        model = Project
        fields = ['title', 'type', 'description', 'tech_stack', 'github_url', 'live_url', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g., Career Tracker Web App',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none text-lg font-medium'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
            'description': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Brief description of your project, challenges overcome, features built...',
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none resize-none'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-6 py-4 border-2 border-gray-300 rounded-xl focus:border-primary focus:outline-none'
            }),
        }
        labels = {
            'title': 'Project Title',
            'type': 'Project Type',
            'description': 'Description',
            'tech_stack': 'Tech Stack',
            'github_url': 'GitHub URL (Optional)',
            'live_url': 'Live Demo URL (Optional)',
            'status': 'Status',
        }