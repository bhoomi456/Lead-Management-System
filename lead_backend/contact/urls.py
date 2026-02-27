from django.urls import path
from .views import contact_message

urlpatterns = [
    path('', contact_message),
]
