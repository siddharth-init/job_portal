from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):

    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("recruiter", "Recruiter"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="candidate")

    resume = models.FileField(upload_to="resumes/", null=True, blank=True)

    bio = models.TextField(null=True, blank=True)

    def __str__(self):

        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, raw, **kwargs):
    """
    raw=True during loaddata

    Skip profile creation while importing fixtures
    """

    if raw:

        return

    if created:

        Profile.objects.create(user=instance)
