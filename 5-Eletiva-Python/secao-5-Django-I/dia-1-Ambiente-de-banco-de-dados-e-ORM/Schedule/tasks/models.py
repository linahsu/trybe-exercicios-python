from django.db import models

class Task(models.Model):
  class Priority(models.IntegerChoices):
    BAIXA = 1, 'Baixa'
    MEDIA = 2, 'Média'
    ALTA = 3, 'Alta'
    
  title = models.CharField(max_length=200)
  description = models.TextField()
  due_date = models.DateField()
  completed = models.BooleanField(default=False)
  priority = models.IntegerChoices(choices=Priority.choices, default=Priority.BAIXA)
  created_at = models.DateTimeField(auto_now_add=True)
