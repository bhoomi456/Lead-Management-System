from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from leads.models import Lead
from tasks.models import Task
from users.models import UserRole
from .utils import send_notification_email


# -----------------------------------------------------
# 1️⃣ USER REGISTERED → SEND EMAIL
# -----------------------------------------------------
@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Lead Management System"
        message = f"Hello {instance.username},\n\nYour account has been created successfully."
        send_notification_email(instance.email, subject, message)


# -----------------------------------------------------
# 2️⃣ LEAD ASSIGNED → NOTIFY ASSIGNED USER
# -----------------------------------------------------
@receiver(post_save, sender=Lead)
def send_lead_assigned_email(sender, instance, created, **kwargs):
    if instance.assigned_to:        # Make sure lead is assigned
        user_role = instance.assigned_to
        email = user_role.user.email

        subject = f"New Lead Assigned: {instance.name}"
        message = (
            f"Hello {user_role.user.username},\n\n"
            f"You have been assigned a new lead.\n"
            f"Lead Name: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Phone: {instance.phone}\n\n"
            f"Please follow up accordingly."
        )

        send_notification_email(email, subject, message)


# -----------------------------------------------------
# 3️⃣ TASK ASSIGNED → NOTIFY ASSIGNED USER
# -----------------------------------------------------
@receiver(post_save, sender=Task)
def send_task_assigned_email(sender, instance, created, **kwargs):
    if instance.assigned_to:        # Task is assigned
        user_role = instance.assigned_to
        email = user_role.user.email

        subject = f"New Task Assigned: {instance.title}"
        message = (
            f"Hello {user_role.user.username},\n\n"
            f"You have been assigned a task.\n"
            f"Task Title: {instance.title}\n"
            f"Status: {instance.status}\n"
            f"Due Date: {instance.due_date}\n\n"
            f"Please check your task list."
        )

        send_notification_email(email, subject, message)
