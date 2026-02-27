from django.db import models
# from django.contrib.auth.models import User

from users.models import UserRole   



# Create your models here.

# Task Model



# Task Category
class TaskCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'tasks' 

    def __str__(self):
        return self.name


# Task Label
class TaskLabel(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        app_label = 'tasks'


    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(TaskCategory, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.ForeignKey(TaskLabel, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    due_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    ], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     app_label = 'tasks'

    def __str__(self):
        return self.title

# Create your models here.

# Task Model
