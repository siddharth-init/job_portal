from turtle import title

from django import forms
from .models import Application
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = ["title", "company_name", "location", "salary", "description"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter job title"}
            ),
            "company_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter company name"}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter location"}
            ),
            "salary": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter salary"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Enter job description",
                }
            ),
        }


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ["cover_letter"]
