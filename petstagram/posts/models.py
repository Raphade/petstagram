from django.db import models
from users_pet.models import Profile
from django.utils import timezone

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "static/user_{0}/{1}".format(instance.poster.user.id, filename)
# Create your models here.
class Post(models.Model):
    poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post_likes = models.ManyToManyField(Profile, related_name='liked_posts')
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    media = models.ImageField(upload_to=user_directory_path)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    commenter = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment_likes = models.ManyToManyField(Profile, related_name='liked_comments')
    text = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(null=True)
