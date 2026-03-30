
from django.urls import path

from .views import create_profile

urlpatterns = [
    path('profile/',create_profile,name='candidate_profile')
]
