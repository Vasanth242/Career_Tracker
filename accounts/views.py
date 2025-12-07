# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from django_ratelimit import UNSAFE
from .models import Profile
from .forms import ProfileForm

# ==========================
# REGISTRATION
# ==========================
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-create profile with defaults
            Profile.objects.create(
                user=user,
                name=user.username,
                current_role="Software Engineer",
                target_countries=['Singapore', 'Germany', 'Finland', 'Switzerland'],
                preferred_roles=['Software Engineer', 'Backend Developer', 'SDET', 'QA Automation'],
                key_skills=['Python', 'Django', 'Robot Framework', 'SQL', 'Automation Testing'],
                email_notifications=True
            )
            
            login(request, user)
            messages.success(request, "Welcome! Let's set up your job preferences →")
            return redirect('settings')
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})


# ==========================
# LOGIN (Protected from Brute Force)
# ==========================
@ratelimit(key='ip', rate='5/m', method=UNSAFE, block=True)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})


# ==========================
# LOGOUT
# ==========================
def logout_view(request):
    logout(request)
    messages.success(request, "You've been logged out securely.")
    return redirect('login')


# ==========================
# RATE LIMIT ERROR PAGE
# ==========================
def rate_limited(request, exception=None):
    messages.error(request, "Too many login attempts. Please wait 1 minute and try again.")
    return render(request, 'login.html', {'form': AuthenticationForm()})


# ==========================
# SETTINGS / PROFILE (Beautiful + Functional)
# ==========================
@login_required
def settings_view(request):
    # Auto-create profile if missing (100% safe)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if created:
        messages.info(request, "Profile created! Please fill in your details.")

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile saved! Fetching your dream jobs now...")
            
            # Trigger job fetch with updated skills
            try:
                from jobs.tasks import fetch_jobs
                fetch_jobs.delay()  # Background (safe)
            except:
                fetch_jobs()  # Fallback sync
            
            return redirect('jobs')
    else:
        # Pre-fill comma-separated fields for easy editing
        initial_data = {
            'target_countries': ', '.join(profile.target_countries) if profile.target_countries else '',
            'preferred_roles': ', '.join(profile.preferred_roles) if profile.preferred_roles else '',
            'key_skills': ', '.join(profile.key_skills) if profile.key_skills else '',
        }
        form = ProfileForm(instance=profile, initial=initial_data)

    return render(request, 'settings.html', {
        'form': form,
        'profile': profile
    })