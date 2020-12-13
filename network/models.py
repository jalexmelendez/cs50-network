from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class user_rel(models.Model):
    user = models.CharField(max_length=225)
    followers_json = models.CharField(max_length=225)
    follows_json = models.CharField(max_length=225)

class post(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='post_id')
    user = models.CharField(max_length=225)
    date = models.CharField(max_length=225)
    image_url = models.CharField(max_length=225)
    body = models.CharField(max_length=225)
    like_count = models.CharField(max_length=12, null=True)
    dislike_count = models.CharField(max_length=12, null=True)
