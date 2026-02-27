from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserRole

# class UserCreateSerializer(serializers.ModelSerializer):
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     role = serializers.CharField()

#     class Meta:
#         model = UserRole
#         fields = ['id', 'username', 'email', 'password', 'role']

#     def create(self, validated_data):
#         username = validated_data.pop("username")
#         email = validated_data.pop("email")
#         password = validated_data.pop("password")
#         role = validated_data.pop("role", "employee")

#         user = User.objects.create_user(
#             username=username,
#             email=email,
#             password=password
#         )

#         user_role = UserRole.objects.create(
#             user=user,
#             role=role
#         )

#         return user_role
    

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False, default='employee')

    class Meta:
        model = UserRole
        fields = ["id", "username", "email", "password", "role"]

    def create(self, validated_data):
        username = validated_data.pop("username")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        role = validated_data.pop("role", "employee")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user_role = UserRole.objects.create(
            user=user,
            role=role
        )

        return user_role

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    date_joined = serializers.DateTimeField(source='user.date_joined')

    class Meta:
        model = UserRole
        fields = ['id', 'username', 'email', 'role', 'date_joined']

class UserRoleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserRole
        fields = ['id', 'username', 'role']
