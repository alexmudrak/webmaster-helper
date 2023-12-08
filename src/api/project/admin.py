from django.contrib import admin

from api.project.models import Project


@admin.register(Project)
class UserAdmin(admin.ModelAdmin):
    pass
