from django.urls import path


from .views import lead_report, followup_report, task_report

urlpatterns = [
    path('leads/', lead_report),
    path('followup-report/', followup_report),
    path('tasks-report/', task_report),
]
