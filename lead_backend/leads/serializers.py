from rest_framework import serializers

from users.serializers import UserSerializer,UserRoleSerializer

# from lead_backend.tasks.serializers import UserRoleSerializer
from .models import Lead
from .models import FollowUp
# from django.contrib.auth.models import User
from users.models import UserRole   
from django.contrib.auth.models import User



class FollowUpSerializer(serializers.ModelSerializer):
    lead_name = serializers.CharField(source='lead.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = FollowUp
        fields = '__all__'

class LeadSerializer(serializers.ModelSerializer):
    followups = FollowUpSerializer(many=True, read_only=True)
    assigned_to = UserRoleSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=UserRole.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False
    )


    class Meta:
        model = Lead
        fields = "__all__"


