from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from skills.models import Skill


class Job(models.Model):
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    required_skills = models.ManyToManyField(Skill)

    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Application(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
    )

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"  

    
