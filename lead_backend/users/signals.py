from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from notifications.utils import send_notification_email
from .models import UserRole

@receiver(post_save, sender=User)
def create_user_role(sender, instance, created, **kwargs):
    if created:
        UserRole.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_notification_email(
            instance.email,
            "Welcome to CRM",
            f"Hello {instance.username}, your account has been created successfully!"
        )