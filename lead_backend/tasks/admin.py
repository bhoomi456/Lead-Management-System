from django.contrib import admin
from .models import TaskCategory, TaskLabel, Task

admin.site.register(TaskCategory)
admin.site.register(TaskLabel)
admin.site.register(Task)

# Register your models here.
