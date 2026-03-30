from .models import  CandidateProfile

def user_profile(request):
    if request.user.is_authenticated:
        profile =  CandidateProfile.objects.filter(user=request.user).first()
        return {'profile': profile}
    return {'profile': None}

