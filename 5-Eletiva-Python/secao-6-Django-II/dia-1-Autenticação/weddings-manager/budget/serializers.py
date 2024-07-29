from rest_framework import serializers
from budget.models import Vendor, Marriage, Budget


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "price"]


class BudgetSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "vendors", "marriage"]


class NestedBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ["id", "vendors"]


class MarriageSerializer(serializers.ModelSerializer):
    budget = NestedBudgetSerializer()

    class Meta:
        model = Marriage
        fields = ["id", "codename", "date", "budget"]

    def create(self, validated_data):
        budget_data = validated_data.pop('budget')
        budget_data['marriage'] = Marriage.objects.create(**validated_data)
        BudgetSerialiser().create(validated_data=budget_data)
        return budget_data['marriage']


class AdminVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_superuser:
            return super().create(validated_data)
        raise serializers.ValidationError(
            "Você não tem permissão para criar fornecedores."
        )
