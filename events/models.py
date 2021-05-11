from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image


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


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @receiver(post_save, sender=CustomUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=CustomUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
