from django.db import models
# from django.contrib.auth.models import User
from users.models import UserRole   


class Lead(models.Model):
    STATUS_CHOICES = (
        ('new' , 'New'),
        ('contracted' , 'Contracted'),
        ('qualified' , 'Qualified'),
        ('converted' , 'Converted'),
        ('lost' , 'Lost'),
    )
    SOURCE_CHOICES = (
        ('google', 'Google Ads'),
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('linkedin', 'LinkedIn'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    lead_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='other')

    notes = models.TextField(blank=True, null=True)
    assigned_to = models.ForeignKey(
        UserRole,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
# Create your models here.

class FollowUp(models.Model):
    lead = models.ForeignKey(Lead, on_delete = models.CASCADE, related_name="followups")
    date = models.DateField()
    remarks = models.TextField(blank=True, null=True)
    next_followup = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank= True,related_name="created_followups")
    created_by = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, blank=True,related_name="assigned_followups")

    def __str__(self):
        return f"FollowUp for {self.lead.name} on {self.date}"
