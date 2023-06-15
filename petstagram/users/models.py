from django.db import models
from django.contrib.auth.models import User
from django import forms


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True, blank=True)
    subscribed = models.ManyToManyField('self', symmetrical=False, blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pics', default='/static/profile_pics/default.jpg', blank=True)

    def __str__(self):
        return self.user.username

