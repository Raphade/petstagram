from django.db import models
from users.models import Profile

# Create your models here.
class Post(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_likes = models.ManyToManyField(Profile, related_name = 'liked_posts')
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True)
    media = models.ImageField(upload_to='posts_pics')
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_likes = models.ManyToManyField(Profile, related_name = 'liked_comments')
    text = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True)
