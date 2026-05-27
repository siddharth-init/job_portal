from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

ROLE_CHOICES = (
    ("candidate", "Candidate"),
    ("recruiter", "Recruiter"),
)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["resume", "bio"]


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    role = forms.ChoiceField(
        choices=ROLE_CHOICES, widget=forms.RadioSelect, required=True
    )

    class Meta:

        model = User

        fields = [
            "username",
            "email",
            "role",
            "password1",
            "password2",
        ]
