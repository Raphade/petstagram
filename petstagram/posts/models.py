from django.db import models

# Create your models here.
class Post(models.Model):
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True)

class Comment(models.Model):
    text = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True)
