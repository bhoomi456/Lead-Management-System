from django.core.mail import send_mail
from django.conf import settings

def send_contact_email(name, email, message):
    subject = f"New Contact Form Message from {name}"
    body = f"""
    Name: {name}
    Email: {email}
    Message:
    {message}
    """
    
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,     # sender
        [settings.EMAIL_HOST_USER],   # receiver (you)
        fail_silently=False
    )
