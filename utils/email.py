from django.conf import settings
from django.core.mail import send_mail


def send_application_status_email(application):

    candidate_email = application.user.email

    candidate_name = application.user.username

    job_title = application.job.title

    status = application.status

    if status == "shortlisted":

        subject = "Application Shortlisted"

        message = f"""
Hello {candidate_name},

Congratulations!

You have been shortlisted for the position:

{job_title}

The recruiter may contact you soon.

Best regards,
Job Portal Team
"""

    elif status == "rejected":

        subject = "Application Update"

        message = f"""
Hello {candidate_name},

Thank you for applying for:

{job_title}

Unfortunately, you were not selected for this position.

We wish you success in your future applications.

Best regards,
Job Portal Team
"""

    else:

        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [candidate_email],
        fail_silently=False,
    )
