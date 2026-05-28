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

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Enter your email"}
        ),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        required=True,
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

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter username"}
        )
        self.fields["password1"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Enter password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Confirm password"}
        )
