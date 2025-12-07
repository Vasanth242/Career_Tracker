# accounts/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    # Comma-separated inputs (user-friendly)
    target_countries = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Singapore, Germany, Finland, Switzerland',
            'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
        }),
        help_text="Separate countries with commas"
    )
    preferred_roles = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Software Engineer, Backend Developer, SDET, QA Automation',
            'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
        }),
        help_text="e.g., SDET, Full Stack Developer"
    )
    key_skills = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, Django, Robot Framework, SQL, Automation Testing',
            'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
        }),
        help_text="Your strongest skills — the more, the better jobs we find!"
    )

    reminder_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}, format='%H:%M'),
        initial='21:00',
        help_text="Daily study & apply reminder (e.g., 9:00 PM)"
    )

    class Meta:
        model = Profile
        fields = [
            'name',
            'current_role',
            'target_countries',
            'preferred_roles',
            'key_skills',
            'email_notifications',
            'reminder_time'
        ]
        widgets = {
            'current_role': forms.TextInput(attrs={
                'placeholder': 'Software Engineer',
                'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'name': forms.TextInput(attrs={
                'placeholder': 'Your Full Name',
                'class': 'w-full px-4 py-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary'
            }),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'w-5 h-5 text-primary'}),
        }

    # Convert comma-separated strings → Python lists
    def clean_target_countries(self):
        data = self.cleaned_data['target_countries']
        return [item.strip() for item in data.split(',') if item.strip()]

    def clean_preferred_roles(self):
        data = self.cleaned_data['preferred_roles']
        return [item.strip() for item in data.split(',') if item.strip()]

    def clean_key_skills(self):
        data = self.cleaned_data['key_skills']
        return [item.strip() for item in data.split(',') if item.strip()]