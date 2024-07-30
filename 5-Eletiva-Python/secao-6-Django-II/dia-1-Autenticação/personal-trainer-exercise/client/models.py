from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    personal_trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="client",
    )

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="workout_plan"
    )
    personal_trainer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workout_plan"
    )
    workout = models.TextField()

    def __str__(self):
        return (f"{self.client} - "
                f"personal-trainer: {self.personal_trainer.get_username()}")
