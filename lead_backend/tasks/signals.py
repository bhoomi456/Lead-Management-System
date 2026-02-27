from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Task
from notifications.utils import send_notification_email

@receiver(post_save, sender=Task)
def notify_assigned_task(sender, instance, created, **kwargs):
    if instance.assigned_to:
        user = instance.assigned_to.user
        send_notification_email(
            user.email,
            "New Task Assigned",
            f"Hello {user.username},\n\nTask '{instance.title}' has been assigned to you.\nDue Date: {instance.due_date}"
        )
