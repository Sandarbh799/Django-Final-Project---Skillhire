from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import RegisterForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from interviews.models import Interview


def home_view(request):
    return render(request,'home.html')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:   
        form = RegisterForm()
    
    return render(request,'accounts/register.html',{'form':form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'candidate':
                return redirect('candidate_dashboard')
            elif user.role == 'recruiter':
                return redirect('recruiter_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


@login_required
def candidate_dashboard(request):

    # 🔒 Role protection (important)
    if request.user.role != 'candidate':
        return redirect('login')

    # 🎯 Interview data
    interviews = Interview.objects.filter(
        candidate=request.user,
        status='scheduled'
    )

    return render(request, 'accounts/candidate_dashboard.html', {
        'interviews': interviews
    })

@login_required
def recruiter_dashboard(request):
    if request.user.role != 'recruiter':
        return redirect('login')
    return render(request, 'accounts/recruiter_dashboard.html')

def logout_view(request):
    logout(request)
    return redirect('/')



