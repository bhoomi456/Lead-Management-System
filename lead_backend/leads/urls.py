from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeadViewSet, FollowUpViewSet, RegisterView
from . import views
router = DefaultRouter()
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'followups', FollowUpViewSet, basename='followup')

urlpatterns = [
    path('', include(router.urls)),
    path('/auth/register/', RegisterView.as_view(), name='register'),
    path('dashboard/', views.dashboard_data, name='dashboard_data'),
    path('dashboard/lead-status-summary/', views.lead_status_summary, name='lead-status-summary'),


]
