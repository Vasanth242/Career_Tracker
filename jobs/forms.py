from django import forms
from .models import JobSource, Job

class JobSourceForm(forms.ModelForm):
    class Meta:
        model = JobSource
        fields = ['country', 'label', 'job_search_url']

class JobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['status']