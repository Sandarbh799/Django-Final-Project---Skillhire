from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from skills.models import Skill
from accounts.models import CustomUser

class CandidateProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    phone = models.CharField(max_length=15, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    experience = models.IntegerField(default=0, null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.ManyToManyField('skills.Skill')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    def __str__(self):
        return self.user.username