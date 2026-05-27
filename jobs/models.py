from venv import create

from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    posted_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posted_jobs", null=True
    )
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    description = models.TextField()
    saved_by = models.ManyToManyField(User, related_name="saved_jobs", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    status_choices = (
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=status_choices, default="pending")

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"
