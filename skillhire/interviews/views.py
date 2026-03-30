from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import InterviewForm
from .models import Interview
from jobs.models import Job
from accounts.models import CustomUser


from django.contrib import messages

@login_required
def schedule_interview(request, job_id, candidate_id):

    job = get_object_or_404(Job, id=job_id)
    candidate = get_object_or_404(CustomUser, id=candidate_id)

    # 🔥 Duplicate check
    if Interview.objects.filter(job=job, candidate=candidate).exists():
        messages.error(request, "Interview already scheduled for this candidate!")
        return redirect('recruiter_dashboard')

    if request.method == 'POST':
        form = InterviewForm(request.POST)

        if form.is_valid():
            interview = form.save(commit=False)
            interview.job = job
            interview.candidate = candidate
            interview.save()

            messages.success(request, "Interview scheduled successfully!")
            return redirect('recruiter_dashboard')

    else:
        form = InterviewForm()

    return render(request, 'interviews/schedule.html', {'form': form})


@login_required
def accept_interview(request, interview_id):

    interview = get_object_or_404(Interview, id=interview_id, candidate=request.user)
    interview.status = 'accepted'
    interview.save()

    return redirect('my_interviews')


@login_required
def reject_interview(request, interview_id):

    interview = get_object_or_404(Interview, id=interview_id, candidate=request.user)
    interview.status = 'rejected'
    interview.save()

    return redirect('my_interviews')

@login_required
def my_interviews(request):

    interviews = Interview.objects.filter(candidate=request.user)

    return render(request, 'interviews/my_interviews.html', {'interviews': interviews})