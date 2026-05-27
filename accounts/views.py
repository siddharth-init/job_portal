import re

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from jobs.models import Application
from .forms import ProfileForm
from jobs.models import Job, Application
from django.db.models import Count

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .forms import RegisterForm

# Create your views here.


def home(request):
    return render(request, "accounts/home.html")


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            """
            Save selected role
            """
            role = form.cleaned_data.get("role")
            user.profile.role = role
            user.profile.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created successfully for {username}")
            return redirect("home")

    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome {username}")
                return redirect("home")

    else:
        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully")
    return redirect("home")


# @login_required
# def dashboard(request):
#     applications = Application.objects.filter(user=request.user).order_by("-applied_at")
#     saved_jobs = request.user.saved_jobs.all()
#     return render(
#         request,
#         "accounts/dashboard.html",
#         {"applications": applications, "saved_jobs": saved_jobs},
#     )


@login_required
def dashboard(request):

    if request.user.profile.role == "recruiter":
        jobs = Job.objects.filter(posted_by=request.user)
        total_jobs = jobs.count()
        applications = Application.objects.filter(job__posted_by=request.user)
        total_applications = applications.count()
        shortlisted_count = applications.filter(status="shortlisted").count()
        rejected_count = applications.filter(status="rejected").count()
        recent_jobs = jobs.order_by("-created_at")[:5]
        recent_applications = applications.order_by("-applied_at")[:5]
        return render(
            request,
            "accounts/recruiter_dashboard.html",
            {
                "total_jobs": total_jobs,
                "total_applications": total_applications,
                "shortlisted_count": shortlisted_count,
                "rejected_count": rejected_count,
                "recent_jobs": recent_jobs,
                "recent_applications": recent_applications,
            },
        )

    applications = Application.objects.filter(user=request.user).order_by("-applied_at")
    saved_jobs = request.user.saved_jobs.all()
    return render(
        request,
        "accounts/dashboard.html",
        {
            "applications": applications,
            "saved_jobs": saved_jobs,
        },
    )


@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profile updated successfully")
            return redirect("profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "accounts/profile.html", {"form": form, "profile": profile})


def candidate_profile(request, user_id):

    candidate = get_object_or_404(User, id=user_id)

    return render(request, "accounts/candidate_profile.html", {"candidate": candidate})
