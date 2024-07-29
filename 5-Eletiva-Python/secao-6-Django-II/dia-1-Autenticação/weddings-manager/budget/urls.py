from rest_framework import routers
from django.urls import path, include
from budget.views import VendorViewSet, MarriageViewSet, BugdetViewSet


router = routers.DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'marriages', MarriageViewSet)
router.register(r'budgets', BugdetViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
