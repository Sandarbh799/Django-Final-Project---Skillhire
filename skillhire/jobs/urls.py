
from django.urls import path

from .views import create_job
from .views import recruiter_jobs
from .views import edit_job
from .views import delete_job
from .views import job_list
from .views import apply_job
from .views import job_applicants
from .views import all_applicants
from .views import update_application_status
from .views import my_applications


urlpatterns = [
    path('create/',create_job,name='create_job'),
    path('my-jobs/',recruiter_jobs,name='recruiter_jobs'),
    path('edit/<int:job_id>/',edit_job,name='edit_job'),
    path('delete/<int:job_id>/',delete_job,name='delete_job'),
    path('all/',job_list,name='job_list'),
    path('apply/<int:job_id>/',apply_job,name='apply_job'),
    path('applicants/<int:job_id>/',job_applicants,name='job_applicants'),
    path('all-applicants/', all_applicants, name='all_applicants'),
    path('update-status/<int:app_id>/<str:status>/', update_application_status, name='update_status'),
    path('my-applications/', my_applications, name='my_applications'),
]