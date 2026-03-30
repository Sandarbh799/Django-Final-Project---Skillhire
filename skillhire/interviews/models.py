from django.db import models
from django.conf import settings
from jobs.models import Job


class Interview(models.Model):

    MODE_CHOICES = (
        ('online', 'Online'),
        ('offline', 'Offline'),
    )

    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    date = models.DateField()
    time = models.TimeField()

    mode = models.CharField(max_length=20, choices=MODE_CHOICES)

    meeting_link = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')

    created_at = models.DateTimeField(auto_now_add=True)

    # 🔥 IMPORTANT (Duplicate prevention)
    class Meta:
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate.username} - {self.job.title}"