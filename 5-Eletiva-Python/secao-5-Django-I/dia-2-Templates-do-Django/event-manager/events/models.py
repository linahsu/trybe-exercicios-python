from django.db import models


class Event(models.Model):
    TYPE_CHOICES = (
        ('C', 'Conference'),
        ('S', 'Seminar'),
        ('W', 'Workshop'),
        ('O', 'Other'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=50,
    )
    is_remote = models.BooleanField(default=False)
    image = models.ImageField(upload_to='events/img', blank=True)

    def __str__(self):
        return f'{self.title} - {self.date} - {self.location}'
