"""
URL configuration for lead_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from leads.views import FollowUpViewSet, LeadViewSet , RegisterView, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from tasks.views import TaskLabelViewSet,TaskCategoryViewSet,TaskViewSet

router = routers.DefaultRouter()
router.register(r'leads', LeadViewSet,basename='lead')
router.register(r'followups', FollowUpViewSet)
router.register(r'users', UserViewSet, basename='user')
# router.register(r'tasks', TaskViewSet)
# router.register(r'categories', TaskCategoryViewSet)
# router.register(r'labels', TaskLabelViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),

    path('api/', include(router.urls)),
    path('api/', include('leads.urls')),
    path('api/', include('tasks.urls')),  
    

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/reports/', include('reports.urls')),
    path('api/contact/', include('contact.urls')),

    


]
