# jobs/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from career_tracker import settings
from .models import Job
from .forms import JobStatusForm
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


# ==========================
# 1. Generate Tailored CV (AJAX)
# ==========================
@login_required
@csrf_exempt
def generate_cv(request, job_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})

    try:
        job = request.user.jobs.get(pk=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Job not found'})

    profile = request.user.profile

    prompt = f"""
    Generate a professional, ATS-friendly CV in clean Markdown format.

    Candidate Profile:
    - Name: {profile.name or request.user.get_full_name() or request.user.username}
    - Current Role: {profile.current_role}
    - Key Skills: {', '.join(profile.key_skills)}
    - Target Roles: {', '.join(profile.preferred_roles)}

    Target Job:
    - Title: {job.title}
    - Company: {job.company}
    - Location: {job.location}
    - Skills Required: {', '.join(job.tags)}
    - Job Description: {job.description[:3000]}

    Requirements:
    - Tailor perfectly to this job
    - Strong opening summary
    - Highlight matching skills first
    - Use clean Markdown (##, -, **bold**, etc.)
    - Output ONLY the CV — no extra text
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1400,
            temperature=0.7
        )
        cv_content = response.choices[0].message.content.strip()

        return JsonResponse({
            'success': True,
            'cv_content': cv_content,
            'job_title': job.title
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': f"OpenAI error: {str(e)}"})


# ==========================
# 2. Generate Tailored Cover Letter (AJAX)
# ==========================
@login_required
@csrf_exempt
def generate_cover_letter_ajax(request, job_id):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'POST required'})

    try:
        job = request.user.jobs.get(pk=job_id)
    except Job.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Job not found'})

    profile = request.user.profile

    prompt = f"""
    Write a compelling, professional cover letter in plain text (no Markdown) for:

    Name: {profile.name or request.user.username}
    Current Role: {profile.current_role}
    Key Skills: {', '.join(profile.key_skills)}

    Applying for:
    Job Title: {job.title}
    Company: {job.company}
    Location: {job.location}

    Job Description (summary): {job.description[:2500]}

    Instructions:
    - Sound confident and enthusiastic
    - Highlight 2–3 strongest matching skills
    - Mention why they're excited about this company/role
    - End with a strong call to action
    - Keep under 400 words
    - Natural, human tone
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert career coach writing winning cover letters."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=700,
            temperature=0.8
        )
        cover_letter = response.choices[0].message.content.strip()

        return JsonResponse({
            'success': True,
            'cover_letter': cover_letter,
            'job_title': job.title
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def jobs_list(request):
    """
    Show all jobs for the current user with optional filters
    """
    jobs = Job.objects.filter(user=request.user).order_by('-date_posted')

    # Filters
    status = request.GET.get('status')
    country = request.GET.get('country')
    source = request.GET.get('source')

    if status and status != 'all':
        jobs = jobs.filter(status=status)
    if country:
        jobs = jobs.filter(location__icontains=country)
    if source:
        jobs = jobs.filter(source__icontains=source)

    all_jobs = Job.objects.filter(user=request.user)
    context = {
        'jobs': jobs,
        'total_jobs': jobs.count(),
        'new_jobs_count': all_jobs.filter(status='new').count(),
        'saved_jobs_count': all_jobs.filter(status='saved').count(),
        'applied_jobs_count': all_jobs.filter(status='applied').count(),
        'ignored_jobs_count': all_jobs.filter(status='ignored').count(),
        'status_filter': status or 'all',
        'country_filter': country or '',
        'source_filter': source or '',
    }
    return render(request, 'jobs.html', context)


@login_required
def job_update_status(request, pk):
    """
    Update job status (New → Saved → Applied → Ignored)
    """
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == 'POST':
        form = JobStatusForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job status updated to '{job.get_status_display()}'")
            return redirect('jobs')
    else:
        form = JobStatusForm(instance=job)

    return render(request, 'job_update.html', {'form': form, 'job': job})


@login_required
def job_mark_applied(request, pk):
    """
    Quick action: Mark as Applied with one click
    """
    job = get_object_or_404(Job, pk=pk, user=request.user)
    job.status = 'applied'
    job.save()
    messages.success(request, f"Marked '{job.title}' as Applied!")
    return redirect('jobs')


@login_required
def job_delete(request, pk):
    """
    Remove a job (rarely used, but helpful)
    """
    job = get_object_or_404(Job, pk=pk, user=request.user)
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f"Removed '{job_title}' from your list.")
        return redirect('jobs')
    return render(request, 'job_confirm_delete.html', {'job': job})