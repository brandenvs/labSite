from django.db import models
from django.contrib.auth.models import User

class Application(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon_id = models.IntegerField()
    theme_id = models.IntegerField()
    title = models.CharField(max_length=35, default='Untitled')
    github_repository = models.CharField(default='Not available', max_length=255)
    status = models.CharField(default='loading', max_length=35) 
