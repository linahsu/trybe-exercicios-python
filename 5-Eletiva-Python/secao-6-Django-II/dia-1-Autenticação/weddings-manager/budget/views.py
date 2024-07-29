# from django.shortcuts import render
from rest_framework import viewsets
from budget.models import Vendor, Marriage, Budget
from rest_framework.authentication import BasicAuthentication
from budget.serializers import (
    VendorSerializer,
    MarriageSerializer,
    BudgetSerializer,
    AdminVendorSerializer,
)
from budget.permissions import IsOwnerOrAdmin


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = AdminVendorSerializer
    authentication_classes = [BasicAuthentication]

    def get_serializer_class(self):
        if self.action in ("create", "destroy", "update"):
            return AdminVendorSerializer
        return VendorSerializer


class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Quem for admin vê todos os casamentos.
        Caso contrário, a pessoa só vê os próprios casamentos.
        """
        if self.request.user.is_superuser:
            return Marriage.objects.all()
        else:
            return Marriage.objects.filter(user=self.request.user)


class BugdetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        """
        Quem for admin vê todos os orçamentos.
        Caso contrário, a pessoa só vê os próprios orçamentos.
        """
        if self.request.user.is_superuser:
            return Budget.objects.all()
        else:
            return Budget.objects.filter(user=self.request.user)
