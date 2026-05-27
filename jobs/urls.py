from django.urls import path
from . import views

urlpatterns = [
    path("", views.JobListView.as_view(), name="job_list"),
    path("<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("<int:id>/apply/", views.apply_job, name="apply_job"),
    path("<int:id>/save/", views.save_job, name="save_job"),
    path("create/", views.CreateJobView.as_view(), name="create_job"),
    path("my-jobs/", views.RecruiterJobsView.as_view(), name="recruiter_jobs"),
    path("edit/<int:pk>/", views.UpdateJobView.as_view(), name="edit_job"),
    path("delete/<int:pk>/", views.DeleteJobView.as_view(), name="delete_job"),
    path(
        "<int:pk>/applicants/",
        views.JobApplicantsView.as_view(),
        name="job_applicants",
    ),
    path(
        "application/<int:application_id>/<str:status>/",
        views.update_application_status,
        name="update_application_status",
    ),
    path(
        "applications/",
        views.RecruiterApplicationsView.as_view(),
        name="recruiter_applications",
    ),
]
