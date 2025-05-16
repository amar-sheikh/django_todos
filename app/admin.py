from django.contrib import admin
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display=('id', 'task_name', 'is_completed')
    list_filter=['is_completed']
    search_fields=('task_name', 'task_description')