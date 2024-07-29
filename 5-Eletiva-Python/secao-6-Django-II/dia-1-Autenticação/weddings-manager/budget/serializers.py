from rest_framework import serializers
from budget.models import Vendor, Marriage, Budget


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "price"]


class MarriageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marriage
        fields = ["id", "codename", "date", "budget"]


class BudgetSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "vendors", "marriage"]
