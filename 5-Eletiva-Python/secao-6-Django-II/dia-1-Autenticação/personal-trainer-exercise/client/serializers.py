from rest_framework import serializers
from client.models import Client, WorkoutPlan


class WorkoutPlanSerializer(serializers.ModelSerializer):
    personal = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkoutPlan
        fields = ["id", "client", "personal", "workout"]


class NestedWorkoutPlanSerializer(serializers.ModelSerializer):
    personal = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkoutPlan
        fields = ["id", "personal", "workout"]


class ClientSerializer(serializers.ModelSerializer):
    workout_plan = NestedWorkoutPlanSerializer()
    personal = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Client
        fields = ["id", "name", "address", "created_at"]

    def create(self, validated_data):
        current_personal = self.context['request'].personal

        workout_data = validated_data.pop('workout_plan')
        workout_data['personal'] = current_personal
        validated_data['personal'] = current_personal

        workout_data['client'] = Client.objects.create(**validated_data)
        WorkoutPlanSerializer().create(validated_data=workout_data)
        return workout_data['client']
