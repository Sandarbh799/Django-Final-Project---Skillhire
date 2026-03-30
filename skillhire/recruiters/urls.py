from django.urls import path
from .views import recruiter_applications

urlpatterns = [
    path('applications/', recruiter_applications, name='recruiter_applications'),
]