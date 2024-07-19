from django.db import models


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    # ingredients: dicionário contendo o ingrediente e quantidade
    ingredients = models.JSONField(default=dict)
    instructions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="media/img", blank=True)

    def __str__(self):
        return self.name
