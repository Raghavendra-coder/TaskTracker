from django.contrib import admin
from .models import *

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'leader')
    filter_horizontal = ('team_members',)


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_name', 'team', 'task_user', 'status', 'started_at')


# Register your models here.


admin.site.register(CustomUser)
admin.site.register(Team, TeamAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(UserRole)