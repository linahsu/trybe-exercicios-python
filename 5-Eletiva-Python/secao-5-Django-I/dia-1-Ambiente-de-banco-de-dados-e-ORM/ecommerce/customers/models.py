from django.db import models

class Customer(models.Model):
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=200)
  phone = models.CharField(max_length=20)