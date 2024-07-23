from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    seller = models.ForeignKey(
        "Seller",
        on_delete=models.CASCADE,
        related_name="products",
    )

    def __str__(self):
        return self.name


class Seller(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Order(models.Model):
    buyer = models.ForeignKey(
        Buyer,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    product = models.ManyToManyField(
        Product,
        related_name="orders"
    )
