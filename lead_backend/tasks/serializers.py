from rest_framework import serializers

from users.models import UserRole
from .models import Task, TaskCategory, TaskLabel
from users.serializers import UserRoleSerializer


class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = '__all__'


class TaskLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskLabel
        fields = '__all__'

# class UserRoleSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username', read_only=True)

#     class Meta:
#         model = UserRole
#         fields = ['id', 'role', 'username']  # user includes username
#         depth = 1  # expands user → username


class TaskSerializer(serializers.ModelSerializer):
    category = TaskCategorySerializer(read_only=True)
    label = TaskLabelSerializer(read_only=True)

    assigned_to = UserRoleSerializer(read_only=True)
    created_by = UserRoleSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskCategory.objects.all(), source='category', write_only=True
    )
    label_id = serializers.PrimaryKeyRelatedField(
        queryset=TaskLabel.objects.all(), source='label', write_only=True
    )
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=UserRole.objects.all(),
        source='assigned_to',
        write_only=True,
        required=False,
        allow_null=True

    )


    class Meta:
        model = Task
        fields = '__all__'
