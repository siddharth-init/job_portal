from django.contrib import admin
from .models import Job, Application


# Register your models here.
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "created_at")


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at")


admin.site.register(Job, JobAdmin)
admin.site.register(Application)
