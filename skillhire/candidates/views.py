from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CandidateProfile
from .forms import CandidateProfileForm

import re


@login_required
def create_profile(request):
    profile, created = CandidateProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.full_name = request.POST.get('full_name')
        profile.gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        
        if not (phone.isdigit() and len(phone) == 10):
            return render(request, 'candidates/profile_form.html', {
                'profile': profile,
                'error': 'Phone number must be 10 digits only'
            })

        profile.phone = phone

        request.user.email = request.POST.get('email')
        request.user.save()

        profile.education = request.POST.get('education')
        
        exp = request.POST.get('experience')
        profile.experience = int(exp) if exp else 0

        profile.dob = request.POST.get('dob') or None
        profile.country = request.POST.get('country')
        profile.state = request.POST.get('state')
        profile.address = request.POST.get('address')
        profile.bio = request.POST.get('bio')

        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')

        if request.FILES.get('resume'):
            profile.resume = request.FILES.get('resume')

        profile.save()

        return redirect('candidate_dashboard')

    return render(request, 'candidates/profile_form.html', {'profile': profile})

from django.db import models
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    regex=r'^\d{10,15}$',
    message="Phone number must contain only digits (10–15 digits)"
)

class Profile(models.Model):
    phone = models.CharField(
        max_length=15,
        validators=[phone_validator]
    )
    
from interviews.models import Interview

@login_required
def candidate_dashboard(request):

    interviews = Interview.objects.filter(
        candidate=request.user,
        status='scheduled'
    )

    return render(request, 'accounts/candidate_dashboard.html', {
        'interviews': interviews
    })