# from django.shortcuts import render
from rest_framework import viewsets
from budget.models import Vendor, Marriage, Budget
from budget.serializers import VendorSerializer, MarriageSerializer, BudgetSerialiser # noqa E501


class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class MarriageViewSet(viewsets.ModelViewSet):
    queryset = Marriage.objects.all()
    serializer_class = MarriageSerializer


class BugdetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerialiser
