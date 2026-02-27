from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from leads.models import Lead, FollowUp
from tasks.models import Task
from users.models import UserRole

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lead_report(request):
    status = request.GET.get('status')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    queryset = Lead.objects.all()

    if status:
        queryset = queryset.filter(status=status)

    if start_date and end_date:
        queryset = queryset.filter(created_at__date__range=[start_date, end_date])

    return Response(list(queryset.values('name', 'email', 'phone', 'status', 'created_at')))

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def followup_report(request):
    lead = request.GET.get('lead')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    qs = FollowUp.objects.all()

    if lead:
        qs = qs.filter(lead_id=lead)

    if start and end:
        qs = qs.filter(date__range=[start, end])

    data = [{
        "lead_name": f.lead.name,
        "date": f.date,
        "remarks": f.remarks
    } for f in qs]

    return JsonResponse(data, safe=False)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def task_report(request):
    assigned_to = request.GET.get('assigned_to')
    status = request.GET.get('status')
    start = request.GET.get('start_date')
    end = request.GET.get('end_date')

    qs = Task.objects.all()

    if assigned_to:
        qs = qs.filter(assigned_to_id=assigned_to)

    if status:
        qs = qs.filter(status=status)

    if start and end:
        qs = qs.filter(due_date__range=[start, end])

    data = [{
        "title": task.title,
        "description": task.description,
        "assigned_to": task.assigned_to.user.username if task.assigned_to else "Unassigned",
        "created_by": task.created_by.user.username if task.created_by else "Unknown",
        "due_date": task.due_date,
        "status": task.status
    } for task in qs]

    return JsonResponse(data, safe=False)
