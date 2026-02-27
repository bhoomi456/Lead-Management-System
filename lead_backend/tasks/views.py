from rest_framework import viewsets , permissions ,status
from rest_framework.response import Response

from users.models import UserRole
from .models import Task,TaskCategory, TaskLabel
from .serializers import TaskSerializer, TaskCategorySerializer, TaskLabelSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically link created_by and assigned_to with UserRole"""
        user = self.request.user
        user_role = UserRole.objects.filter(user=user).first()


        # 🔹 Get UserRole for the logged-in user
        # try:
        #     user_role = UserRole.objects.get(user=user)
        # except UserRole.DoesNotExist:
        #     return Response(
        #         {"error": "UserRole not found for the current user"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # 🔹 Handle assigned_to field (may come from frontend)
        assigned_to_id = self.request.data.get('assigned_to_id')
        assigned_role = None

        if assigned_to_id:
            assigned_role = UserRole.objects.filter(id=assigned_to_id).first()
            if not assigned_role:
                assigned_role = UserRole.objects.filter(user_id=assigned_to_id).first()

        # If not found, try user_id
            
            # try:
            #     # Try interpreting as User ID
            #     assigned_role = UserRole.objects.get(user_id=assigned_to_id)
            # except UserRole.DoesNotExist:
            #     # Try interpreting as UserRole ID (fallback)
            #     assigned_role = UserRole.objects.filter(id=assigned_to_id).first()

        # 🔹 Save task
        serializer.save(
            created_by=user_role,
            assigned_to=assigned_role or user_role  # default = self
        )


    # permission_classes = [permissions.AllowAny] 

class TaskCategoryViewSet(viewsets.ModelViewSet):
    queryset = TaskCategory.objects.all()
    serializer_class = TaskCategorySerializer
    # permission_classes = [permissions.AllowAny]   # 👈 make public temporarily

    permission_classes = [permissions.IsAuthenticated]



class TaskLabelViewSet(viewsets.ModelViewSet):
    queryset = TaskLabel.objects.all()
    serializer_class = TaskLabelSerializer
    # permission_classes = [permissions.AllowAny]   # 👈 make public temporarily

    permission_classes = [permissions.IsAuthenticated]



@api_view(['GET'])
@permission_classes([AllowAny])
def task_status_summary(request):

    data = {
        "Pending": Task.objects.filter(status="pending").count(),
        "In Progress": Task.objects.filter(status="in-progress").count(),
        "Completed": Task.objects.filter(status="completed").count(),
    }
    return Response(data)



# Create your views here.
