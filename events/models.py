from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass


class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField()
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount_of_visitors = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['event_date']


