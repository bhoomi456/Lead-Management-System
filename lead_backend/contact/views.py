from django.conf import settings
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# from .models import ContactMessage
from .serializers import ContactSerializer
from .utils import send_contact_email
from django.core.mail import send_mail


@api_view(['POST'])
@permission_classes([AllowAny])  # anyone can send message
def contact_message(request):
    name = request.data.get("name")
    email = request.data.get("email")
    message = request.data.get("message")

    # Send email
    send_mail(
        subject=f"New Contact Message from {name}",
        message=f"Email: {email}\n\nMessage:\n{message}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],  # YOU will receive mail
        fail_silently=False,
    )

    return Response({"message": "Message sent successfully!"})
# Create your views here.
