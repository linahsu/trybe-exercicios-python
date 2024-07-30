from rest_framework import viewsets
from client.models import Client, WorkoutPlan
from client.serializers import (
    ClientSerializer,
    WorkoutPlanSerializer,
)


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    queryset = WorkoutPlan.objects.all()
    serializer_class = WorkoutPlanSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
