from django.contrib import admin
from tasks.models import Task

admin.site.site_header = "Schedule app - Tasks List"
admin.site.register(Task)
