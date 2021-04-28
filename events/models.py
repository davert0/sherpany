from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class CustomUser(AbstractUser):
    def save(self, *args, **kwargs):
        self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)


class Event(models.Model):
    title = models.CharField(max_length=150, verbose_name='Name')
    description = models.TextField()
    event_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    visitors = models.ManyToManyField(CustomUser, related_name='visitors')

    def get_absolute_url(self):
        return reverse('view_event', kwargs={"event_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ['event_date']

    def has_visitor(self, user):
        return self.visitors.filter(pk=user.pk).exists()




