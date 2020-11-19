from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Post(models.Model):
    post = models.TextField(blank=True)
    post_time = models.DateTimeField(default=timezone.now)
    user_posted = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"id of post: {self.id}, user posted: {self.user_posted}, "\
               f" at {self.post_time}, text of post: {self.post}"

class ProfileFollows(models.Model):
    user_to_follow = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user")