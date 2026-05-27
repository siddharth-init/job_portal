from email.mime import application
import re

from django.shortcuts import redirect, render, get_object_or_404
from .models import Job, Application
from .forms import ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from .forms import JobForm
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Count
from utils.email import send_application_status_email


from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# Create your views here.

"""
Recruiter Section Start 
"""


class RecruiterJobsView(ListView):
    model = Job
    template_name = "jobs/recruiter_jobs.html"
    context_object_name = "jobs"

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = Job.objects.all() # This is same as above line

        queryset = Job.objects.filter(posted_by=self.request.user).annotate(
            applications_count=Count("application")
        )

        keyword = self.request.GET.get("keyword")
        location = self.request.GET.get("location")
        company = self.request.GET.get("company")

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if company:
            queryset = queryset.filter(company_name__icontains=company)

        return queryset


class CreateJobView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = Job
    form_class = JobForm
    template_name = "jobs/create_job.html"
    success_url = reverse_lazy("recruiter_jobs")

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        messages.success(self.request, "Job created successfully")
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.profile.role == "recruiter"  # type: ignore


class UpdateJobView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/edit_job.html"
    success_url = reverse_lazy("recruiter_jobs")
    context_object_name = "job"

    def test_func(self):
        job = self.get_object()
        return (
            self.request.user.profile.role == "recruiter"  # type: ignore
            and job.posted_by == self.request.user  # type: ignore
        )

    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully")
        return super().form_valid(form)


class DeleteJobView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = "jobs/delete_job.html"
    success_url = reverse_lazy("recruiter_jobs")
    context_object_name = "job"

    def test_func(self):
        job = self.get_object()
        return (
            self.request.user.profile.role == "recruiter"  # type: ignore
            and job.posted_by == self.request.user  # type: ignore
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Job deleted successfully")
        return super().delete(request, *args, **kwargs)


class JobApplicantsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Job
    template_name = "jobs/job_applicants.html"
    context_object_name = "job"

    def test_func(self):
        job = self.get_object()  # type: ignore
        return (
            self.request.user.profile.role == "recruiter"  # type: ignore
            and job.posted_by == self.request.user  # type: ignore
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["applications"] = Application.objects.filter(job=self.object)  # type: ignore
        return context


class RecruiterApplicationsView(ListView):
    model = Application
    template_name = "jobs/recruiter_applications.html"
    context_object_name = "applications"

    def get_queryset(self):
        queryset = Application.objects.filter(
            job__posted_by=self.request.user
        ).select_related("job", "user")
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset.order_by("-applied_at")


"""
Recruiter Section End 
"""


class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = Job.objects.all() # This is same as above line
        keyword = self.request.GET.get("keyword")
        location = self.request.GET.get("location")
        company = self.request.GET.get("company")

        if keyword:
            queryset = queryset.filter(title__icontains=keyword)

        if location:
            queryset = queryset.filter(location__icontains=location)

        if company:
            queryset = queryset.filter(company_name__icontains=company)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        saved_job_ids = []
        if self.request.user.is_authenticated:
            saved_job_ids = self.request.user.saved_jobs.values_list("id", flat=True)
        context["saved_job_ids"] = saved_job_ids

        return context


class JobDetailView(DetailView):

    model = Job

    template_name = "jobs/job_detail.html"

    context_object_name = "job"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        job = self.get_object()

        user_application_exists = False

        if self.request.user.is_authenticated:

            user_application_exists = Application.objects.filter(
                user=self.request.user, job=job
            ).exists()

        context["user_application_exists"] = user_application_exists

        return context


@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)
    job = application.job
    if request.user.profile.role != "recruiter" or job.posted_by != request.user:
        messages.error(request, "Unauthorized access")
        return redirect("job_list")
    if status in ["shortlisted", "rejected"]:
        application.status = status
        application.save()

        """
        -------------------------
        EMAIL NOTIFICATION
        -------------------------
        """

        send_application_status_email(application)

        messages.success(request, "Application status updated and email sent")

    return redirect("job_applicants", pk=job.id)  # type: ignore


@login_required
def apply_job(request, id):
    job = get_object_or_404(Job, id=id)

    already_applied = Application.objects.filter(user=request.user, job=job).exists()
    if already_applied:
        messages.warning(request, "You have already applied to this job")
        return redirect("job_detail", pk=job.id)  # type: ignore

    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.user = request.user
            application.save()
            messages.success(request, "You have successfully applied for this job")
            return redirect("job_detail", pk=id)
    else:
        form = ApplicationForm()

    return render(request, "jobs/apply_job.html", {"job": job, "form": form})


@login_required
def save_job(request, id):
    job = get_object_or_404(Job, id=id)
    if request.user in job.saved_by.all():
        job.saved_by.remove(request.user)
        messages.success(
            request, "You have successfully removed this job from your saved jobs"
        )
    else:
        job.saved_by.add(request.user)
        messages.success(request, "You have successfully saved this job")
    return redirect("job_detail", pk=id)
