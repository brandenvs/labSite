from django.db import models

from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    selected_theme = models.CharField(max_length=25, default='light') # Used to track user selected theme

    def update_theme(self, new_theme):
        self.selected_theme = new_theme

    def __str__(self):
        return self.user.username
