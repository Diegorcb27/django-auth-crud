from django.contrib import admin
from .models import Task

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created", ) #me muestra el campo created en el admin
admin.site.register(Task, TaskAdmin)