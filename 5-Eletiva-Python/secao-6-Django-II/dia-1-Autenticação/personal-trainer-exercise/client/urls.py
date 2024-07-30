from rest_framework import routers
from django.urls import path, include
from client.views import (
    ClientViewSet,
    WorkoutPlanViewSet,
)

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'workouts', WorkoutPlanViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
