from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from notifications.utils import send_notification_email

@receiver(post_save, sender=Lead)
def notify_assigned_lead(sender, instance, created, **kwargs):
    if instance.assigned_to:
        user = instance.assigned_to.user
        send_notification_email(
            user.email,
            "New Lead Assigned",
            f"Hello {user.username},\n\nA new lead '{instance.name}' has been assigned to you."
        )
