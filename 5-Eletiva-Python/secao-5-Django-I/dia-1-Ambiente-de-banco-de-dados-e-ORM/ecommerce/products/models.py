from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="media/products", null=True, blank=True
    )
    
# python3 -m pip install Pillow
# Anota aí 📝: Pillow é um pacote Python que adiciona suporte para imagens ao Django. Ele é necessário para que possamos utilizar o campo ImageField.