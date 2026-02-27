from django.shortcuts import render
from rest_framework import viewsets , generics, permissions 
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny

from users.serializers import UserCreateSerializer

from .models import Lead
from tasks.models import Task, TaskCategory, TaskLabel

from .serializers import LeadSerializer
from .models import FollowUp
from .serializers import FollowUpSerializer
from .serializers import UserSerializer
# from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from users.models import UserRole   
from django.db.models import Q



class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.prefetch_related("followups").all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user

    # get UserRole safely
        user_role = UserRole.objects.filter(user=user).first()

    # if no role, show nothing
        if not user_role:
            return Lead.objects.none()

    # employee = only assigned leads
        if user_role.role == "employee":
            return Lead.objects.filter(assigned_to=user_role)

    # admin + manager = all leads
        return Lead.objects.all()


    def perform_create(self, serializer):
        assigned_to_id = self.request.data.get("assigned_to_id")

        assigned_user = None
        if assigned_to_id:
            assigned_user = UserRole.objects.filter(id=assigned_to_id).first()

        serializer.save(assigned_to=assigned_user)

class FollowUpViewSet(viewsets.ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer
    permission_classes = [IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    queryset = UserRole.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]   # ✅ This allows sign-up without login


class UserViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all().order_by('-id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]



@api_view(['GET'])
@permission_classes([AllowAny])  # change to [IsAuthenticated] in production
def dashboard_data(request):
    # -------------------
    # Leads
    # -------------------
    total_leads = Lead.objects.count()
    status_counts = {
        'new': Lead.objects.filter(status='new').count(),
        'contacted': Lead.objects.filter(status='contacted').count(),
        'converted': Lead.objects.filter(status='converted').count(),
        'lost': Lead.objects.filter(status='lost').count(),
    }

    # Lead info (if assigned_to field exists)
    lead_fields = [f.name for f in Lead._meta.get_fields()]
    if 'assigned_to' in lead_fields:
        recent_leads = Lead.objects.order_by('-created_at')[:3].values(
            'name', 'status', 'created_at', 
            'assigned_to__user__username'  # ✅ fix for role-based
        )
    else:
        recent_leads = Lead.objects.order_by('-created_at')[:5 ].values(
            'name', 'status', 'created_at'
        )

    # -------------------
    # FollowUps
    # -------------------
    followup_fields = [f.name for f in FollowUp._meta.get_fields()]
    followup_note_field = 'remarks' if 'remarks' in followup_fields else 'note'
    recent_followups = FollowUp.objects.order_by('-date')[:5].values(
        'lead__name', followup_note_field, 'date'
    )

    # -------------------
    # Tasks
    # -------------------
    task_fields = [f.name for f in Task._meta.get_fields()]
    total_tasks = Task.objects.count() if 'id' in task_fields else 0

    task_status_counts = {}
    for status in ['Pending', 'In Progress', 'Completed']:
        task_status_counts[status] = (
            Task.objects.filter(status=status).count()
            if 'status' in task_fields else 0
        )

    # User-specific tasks (handle UserRole)
    if request.user.is_authenticated and 'assigned_to' in task_fields:
        try:
            user_role = UserRole.objects.get(user=request.user)
            user_tasks = Task.objects.filter(
                Q(assigned_to=user_role) | Q(created_by=user_role)
            ).order_by('-id')[:5].values('title', 'status', 'due_date')

            # user_tasks = Task.objects.filter(assigned_to=user_role).values(
            #     'title', 'status', 'due_date'
            # )
        except UserRole.DoesNotExist:
            user_tasks = []
    else:
        user_tasks = []


    total_users = UserRole.objects.count()
    total_categories = TaskCategory.objects.count()
    total_labels = TaskLabel.objects.count()


    # -------------------
    # Return Response
    # -------------------
    return Response({
        'leads': {
            'total': total_leads,
            'status_counts': status_counts,
            'recent': list(recent_leads)
        },
        'followups': list(recent_followups),
        'tasks': {
            'total': total_tasks,
            'status_counts': task_status_counts,
            'user_tasks': list(user_tasks)
        },
        'total_users': total_users,
        'total_categories': total_categories,
        'total_labels': total_labels

    })


@api_view(['GET'])
@permission_classes([AllowAny]) 
def lead_status_summary(request):

    data = {
        "New": Lead.objects.filter(status="new").count(),

        # contacted + qualified dono ko In Progress count karenge
        "In Progress": Lead.objects.filter(status__in=["contacted", "qualified"]).count(),

        "Converted": Lead.objects.filter(status="converted").count(),
        "Lost": Lead.objects.filter(status="lost").count()
    }

    return Response(data)
