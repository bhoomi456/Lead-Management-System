from django.http import HttpResponse
from django.urls import include, path
from rest_framework import routers
from .views import TaskViewSet, TaskCategoryViewSet, TaskLabelViewSet




# from . import views
# from lead_backend.task import views

router = routers.DefaultRouter()
# router.register(r'', TaskViewSet, basename='tasks_task')
# router.register(r'categories', TaskCategoryViewSet, basename='task-category')
# router.register(r'labels', TaskLabelViewSet, basename='task-label')

router.register(r'tasks', TaskViewSet )
router.register(r'categories', TaskCategoryViewSet)
router.register(r'labels', TaskLabelViewSet)



urlpatterns = [
    # path('test/', lambda request: HttpResponse('Test OK')),

    path('', include(router.urls)),
    # path('', views.TaskViewSet.as_view(), name='task-list'),
    # # path('add/', views.TaskCreateView.as_view(), name='add-task'),
    # path('categories/', views.TaskCategoryViewSet.as_view(), name='task-category'),
    # path('labels/', views.TaskLabelViewSet.as_view(), name='task-label'),

]
