from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField 
from django.utils import timezone

class UserProfile(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    image = models.ImageField(upload_to='files/', default='logo.png', null=True, blank=False)
    country = models.CharField(max_length=200 ,blank=True)

class Poems(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    poem = HTMLField()
    created_on = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_on']


class ImagePoem(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_poem')
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='files/', default='logo.png', null=True, blank=False)
    created_on = models.DateTimeField(default=timezone.now)