from rest_framework import serializers
from client.models import Client, WorkoutPlan


class WorkoutPlanSerializer(serializers.ModelSerializer):
    personal_trainer = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkoutPlan
        fields = ["id", "client", "personal_trainer", "workout"]


class NestedWorkoutPlanSerializer(serializers.ModelSerializer):
    personal_trainer = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = WorkoutPlan
        fields = ["id", "personal_trainer", "workout"]


class ClientSerializer(serializers.ModelSerializer):
    workout_plan = NestedWorkoutPlanSerializer()
    personal_trainer = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "address",
            "created_at",
            "workout_plan",
            "personal_trainer"
        ]

    def create(self, validated_data):
        current_personal = self.context['request'].user

        workout_data = validated_data.pop('workout_plan')
        workout_data['personal_trainer'] = current_personal
        validated_data['personal_trainer'] = current_personal

        workout_data['client'] = Client.objects.create(**validated_data)
        WorkoutPlanSerializer().create(validated_data=workout_data)
        return workout_data['client']
