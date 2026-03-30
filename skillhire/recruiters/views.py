
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def recruiter_applications(request):
    return render(request, 'jobs/job_applicants.html')