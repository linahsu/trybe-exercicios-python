# from django.shortcuts import render
from rest_framework import viewsets
from budget.models import Vendor, Marriage, Budget
from budget.serializers import (
    VendorSerializer,
    MarriageSerializer,
    BudgetSerialiser,
    AdminVendorSerializer,
)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer


class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer


class BugdetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerialiser
