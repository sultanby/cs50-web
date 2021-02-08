from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    profile_pic = models.ImageField(upload_to="images/", null=True, blank=True)

class Post(models.Model):
    post = models.TextField(blank=True)
    post_time = models.DateTimeField(default=timezone.now)
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.ManyToManyField(User, default=0, related_name='like')

    def __str__(self):
        return f"id of post: {self.id}, user posted: {self.user_posted}, "\
               f" at {self.post_time}, text of post: {self.post}, people liked this post: {self.like}"

class ProfileFollows(models.Model):
    user_to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user")