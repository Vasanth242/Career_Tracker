# tracker/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Goals
    path('goals/', views.goals_list, name='goals'),
    path('goal/<int:pk>/edit/', views.goal_edit, name='goal_edit'),
    path('goal/<int:pk>/delete/', views.goal_delete, name='goal_delete'),

    # Tasks (inside a goal)
    path('goal/<int:goal_id>/tasks/', views.tasks_list, name='tasks'),
    path('goal/<int:goal_id>/task/create/', views.task_create, name='task_create'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Courses
    path('courses/', views.courses_list, name='courses'),
    path('course/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('course/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # Projects
    path('projects/', views.projects_list, name='projects'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
]