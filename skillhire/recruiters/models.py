from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings

class RecruiterProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    company_name = models.CharField(max_length=200)
    company_location = models.CharField(max_length=200)
    company_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name