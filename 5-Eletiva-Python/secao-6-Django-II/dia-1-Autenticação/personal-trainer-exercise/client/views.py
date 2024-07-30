from rest_framework import viewsets
from client.models import Client, WorkoutPlan
from client.serializers import (
    ClientSerializer,
    WorkoutPlanSerializer,
)
from client.permissions import IsOwnerOrAdmin


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return WorkoutPlan.objects.all()
        else:
            return WorkoutPlan.objects.filter(
                personal_trainer=self.request.user
            )


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(
                personal_trainer=self.request.user
            )
