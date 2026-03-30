from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Job,Application
from .forms import JobForm


@login_required
def create_job(request):
    if request.user.role != 'recruiter':
        return redirect('login')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            form.save_m2m()
            return redirect('recruiter_jobs')
        
    
    else:
        form = JobForm()
        
    return render(request,'jobs/job_form.html',{'form':form})
        

@login_required
def recruiter_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request,'jobs/recruiter_jobs.html',{'jobs':jobs})

@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('recruiter_jobs')
    else:
        form = JobForm(instance=job)
        
    return render(request,'jobs/job_form.html',{'form':form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    job.delete()
    return redirect('recruiter_jobs')

@login_required
def job_list(request):
    if request.user.role != 'candidate':
        return redirect('login')

    jobs = Job.objects.all().order_by('-posted_at')

    candidate_profile = request.user.candidateprofile
    candidate_skills = candidate_profile.skills.all()

    job_data = []

    for job in jobs:
        required_skills = job.required_skills.all()
        total_required = required_skills.count()

        matched_skills = candidate_skills.filter(id__in=required_skills)
        matched_count = matched_skills.count()

        match_percentage = 0
        if total_required > 0:
            match_percentage = int((matched_count / total_required) * 100)

        job_data.append({
            'job': job,
            'match_percentage': match_percentage
        })

    return render(request, 'jobs/job_list.html', {'job_data': job_data})


@login_required
def apply_job(request, job_id):
    if request.user.role != 'candidate':
        return redirect('login')

    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(candidate=request.user, job=job).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect('job_list')

    Application.objects.create(candidate=request.user, job=job)
    messages.success(request, "Successfully applied to the job!")

    return redirect('job_list')


@login_required
def job_applicants(request, job_id):
    if request.user.role != 'recruiter':
        return redirect('login')

    job = get_object_or_404(Job, id=job_id, posted_by=request.user)
    

    applications = Application.objects.filter(job=job)

    
    applicant_data = []

    for application in applications:
        candidate = application.candidate
        profile = candidate.candidateprofile

        candidate_skills = profile.skills.all()
        required_skills = job.required_skills.all()

        total_required = required_skills.count()
        matched = candidate_skills.filter(id__in=required_skills)
        matched_count = matched.count()

        match_percentage = 0
        if total_required > 0:
            match_percentage = int((matched_count / total_required) * 100)

        applicant_data.append({
            'application': application,
            'candidate': candidate,
            'profile': profile,
            'match_percentage': match_percentage
        })


    return render(request, 'jobs/job_applicants.html', {
        'job': job,
        'applicant_data': applicant_data
    })
    
@login_required
def all_applicants(request):
    if request.user.role != 'recruiter':
        return redirect('login')

    jobs = Job.objects.filter(posted_by=request.user)
    applications = Application.objects.filter(job__in=jobs)

    applicant_data = []

    for application in applications:
        job = application.job

        candidate = application.candidate
        profile = candidate.candidateprofile

        candidate_skills = profile.skills.all()
        required_skills = job.required_skills.all()

        total_required = required_skills.count()
        matched = candidate_skills.filter(id__in=required_skills)
        matched_count = matched.count()

        match_percentage = int((matched_count / total_required) * 100) if total_required > 0 else 0

        applicant_data.append({
            'candidate': candidate,
            'profile': profile,
            'job': job,
            'application': application,   # 🔥 MUST ADD
            'match_percentage': match_percentage
})

    return render(request, 'jobs/all_applicants.html', {
        'applicant_data': applicant_data
    })

@login_required
def update_application_status(request, app_id, status):
    if request.user.role != 'recruiter':
        return redirect('login')

    application = get_object_or_404(Application, id=app_id)

    if application.job.posted_by != request.user:
        return redirect('login')

    application.status = status
    application.save()

    return redirect('job_applicants', job_id=application.job.id)



@login_required
def my_applications(request):
    if request.user.role != 'candidate':
        return redirect('login')

    applications = Application.objects.filter(candidate=request.user).select_related('job')

    application_data = []

    candidate_profile = request.user.candidateprofile
    candidate_skills = candidate_profile.skills.all()

    for app in applications:
        job = app.job
        required_skills = job.required_skills.all()

        total_required = required_skills.count()
        matched = candidate_skills.filter(id__in=required_skills)
        matched_count = matched.count()

        match_percentage = 0
        if total_required > 0:
            match_percentage = int((matched_count / total_required) * 100)

        application_data.append({
            'job': job,
            'status': app.status,
            'applied_at': app.applied_at,
            'match_percentage': match_percentage,
        })

    return render(request, 'jobs/my_applications.html', {
        'application_data': application_data
    })