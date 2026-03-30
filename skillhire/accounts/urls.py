
from django.urls import path    
from .views import home_view, register_view, login_view, logout_view, candidate_dashboard, recruiter_dashboard

urlpatterns = [
    path('',home_view,name='home'),
    path('register/',register_view,name='register'),
    path('login/',login_view,name='login'),
    path('logout/',logout_view,name='logout'),
    path('candidate_dashboard/',candidate_dashboard,name='candidate_dashboard'),
    path('recruiter_dashboard/',recruiter_dashboard,name='recruiter_dashboard')
]
