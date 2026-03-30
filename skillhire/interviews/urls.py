from django.urls import path
from .views import schedule_interview
from .views import accept_interview, reject_interview,my_interviews

urlpatterns = [
    path('schedule/<int:job_id>/<int:candidate_id>/', schedule_interview, name='schedule_interview'),
    path('accept/<int:interview_id>/', accept_interview, name='accept_interview'),
    path('reject/<int:interview_id>/', reject_interview, name='reject_interview'),
    path('my-interviews/', my_interviews, name='my_interviews'),
]
