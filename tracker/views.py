# tracker/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Goal, Task, Course, Project
from .forms import GoalForm, TaskForm, CourseForm, ProjectForm
from jobs.models import Job


@login_required
def dashboard(request):
    goals = Goal.objects.filter(user=request.user).order_by('-target_completion_date')
    tasks_due_soon = Task.objects.filter(
        goal__user=request.user,
        due_date__lte=timezone.now().date() + timedelta(days=7),
        due_date__gte=timezone.now().date(),
        status__in=['not_started', 'in_progress']
    ).count()

    courses_in_progress = Course.objects.filter(user=request.user, status='in_progress').count()
    projects_active = Project.objects.filter(
        user=request.user,
        status__in=['in_planning', 'in_progress']
    ).count()

    new_jobs = Job.objects.filter(user=request.user, status='new').order_by('-date_posted')
    new_jobs_count = new_jobs.count()
    latest_jobs = new_jobs[:6]

    context = {
        'goals': goals,
        'tasks_due_soon': tasks_due_soon,
        'courses_in_progress': courses_in_progress,
        'projects_active': projects_active,
        'latest_jobs': latest_jobs,
        'new_jobs_count': new_jobs_count,
    }
    return render(request, 'dashboard.html', context)


# ========================
# GOALS
# ========================
@login_required
def goals_list(request):
    goals = Goal.objects.filter(user=request.user).order_by('-created_at')
    form = GoalForm()

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            messages.success(request, f"Goal '{goal.title}' created!")
            return redirect('goals')

    return render(request, 'goals.html', {
        'goals': goals,
        'goal_form': form
    })


@login_required
def goal_edit(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, f"Goal '{goal.title}' updated!")
            return redirect('goals')
    else:
        form = GoalForm(instance=goal)
    return render(request, 'goals.html', {
        'goals': Goal.objects.filter(user=request.user),
        'goal_form': form,
        'edit_goal': goal
    })


@login_required
def goal_delete(request, pk):
    goal = get_object_or_404(Goal, pk=pk, user=request.user)
    if request.method == 'POST':
        title = goal.title
        goal.delete()
        messages.success(request, f"Goal '{title}' deleted.")
        return redirect('goals')
    return render(request, 'goals.html', {
        'goals': Goal.objects.filter(user=request.user),
        'delete_goal': goal
    })


# ========================
# TASKS - FULLY WORKING!
# ========================
@login_required
def tasks_list(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id, user=request.user)
    tasks = goal.task_set.all().order_by('due_date')
    return render(request, 'tasks.html', {
        'goal': goal,
        'tasks': tasks
    })


@login_required
def task_create(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.goal = goal
            task.save()
            messages.success(request, "Task added!")
            return redirect('tasks', goal_id=goal_id)
    else:
        form = TaskForm()
    return render(request, 'tasks.html', {
        'goal': goal,
        'tasks': goal.task_set.all(),
        'task_form': form
    })


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, goal__user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated!")
            return redirect('tasks', goal_id=task.goal.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks.html', {
        'goal': task.goal,
        'tasks': task.goal.task_set.all(),
        'task_form': form,
        'edit_task': task
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, goal__user=request.user)
    goal_id = task.goal.id
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted.")
        return redirect('tasks', goal_id=goal_id)
    return render(request, 'tasks.html', {
        'goal': task.goal,
        'tasks': task.goal.task_set.all(),
        'delete_task': task
    })


# ========================
# COURSES
# ========================
@login_required
def courses_list(request):
    courses = Course.objects.filter(user=request.user).order_by('-created_at')
    form = CourseForm()

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            messages.success(request, f"Course '{course.name}' added!")
            return redirect('courses')

    return render(request, 'courses.html', {
        'courses': courses,
        'course_form': form
    })


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Course '{course.name}' updated!")
            return redirect('courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses.html', {
        'courses': Course.objects.filter(user=request.user),
        'course_form': form,
        'edit_course': course
    })


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk, user=request.user)
    if request.method == 'POST':
        name = course.name
        course.delete()
        messages.success(request, f"Course '{name}' deleted.")
        return redirect('courses')
    return render(request, 'courses.html', {
        'courses': Course.objects.filter(user=request.user),
        'delete_course': course
    })


# ========================
# PROJECTS
# ========================
@login_required
def projects_list(request):
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            messages.success(request, f"Project '{project.title}' added!")
            return redirect('projects')

    return render(request, 'projects.html', {
        'projects': projects,
        'project_form': form
    })


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"Project '{project.title}' updated!")
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'projects.html', {
        'projects': Project.objects.filter(user=request.user),
        'project_form': form,
        'edit_project': project
    })


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk, user=request.user)
    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"Project '{title}' deleted.")
        return redirect('projects')
    return render(request, 'projects.html', {
        'projects': Project.objects.filter(user=request.user),
        'delete_project': project
    })