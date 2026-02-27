from django.shortcuts import render
from rest_framework.decorators import api_view , permission_classes
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


from users.models import UserRole   

@api_view(['POST'])
@permission_classes([AllowAny])

def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({'error': 'Invalid credentials'}, status=401)

    # ✅ Role fetch
    role = 'employee'
    try:
        user_role = UserRole.objects.get(user=user)
        role = user_role.role
    except UserRole.DoesNotExist:
        pass

    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'username': user.username,
        'role': user.role.role
    })

# @api_view(['POST'])
# def login_view(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = authenticate(username=username, password=password)
#     if not user:
#         return Response({'error': 'Invalid credentials'}, status=400)

#     # Fetch role from UserRole
#     try:
#         role_obj = UserRole.objects.get(user=user)
#         role = role_obj.role
#     except UserRole.DoesNotExist:
#         role = 'employee'  # default fallback

#     refresh = RefreshToken.for_user(user)

#     return Response({
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#         'username': user.username,
#         'role': role
#     })


# # Create your views here.
