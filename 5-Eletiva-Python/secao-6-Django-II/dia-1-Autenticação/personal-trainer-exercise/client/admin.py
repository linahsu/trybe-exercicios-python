from django.contrib import admin
from client.models import Client, WorkoutPlan


class WorkoutPlanInline(admin.StackedInline):
    model = WorkoutPlan


class ClientAdmin(admin.ModelAdmin):
    inlines = [WorkoutPlanInline]


admin.site.site_header = "Gym Admin Panel"
admin.site.register(Client, ClientAdmin)
