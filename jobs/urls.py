# jobs/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Main Jobs Page
    path('jobs/', views.jobs_list, name='jobs'),

    # Update job status (New → Saved → Applied → Ignored)
    path('job/<int:pk>/update/', views.job_update_status, name='job_update'),

    # One-click "Mark as Applied"
    path('job/<int:pk>/applied/', views.job_mark_applied, name='job_mark_applied'),

    # Delete a job from your list
    path('job/<int:pk>/delete/', views.job_delete, name='job_delete'),

    path('job/<int:job_id>/generate-cv/', views.generate_cv, name='generate_cv'),
    path('job/<int:job_id>/generate-cover-letter/', views.generate_cover_letter_ajax, name='generate_cover_letter'),

    # Optional: Settings page (if you want job sources here)
    # path('settings/', views.settings_view, name='settings'),
]