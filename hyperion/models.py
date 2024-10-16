from django.db import models

class dbStudent(models.Model):
    fullname = models.CharField(max_length=255)
    bootcamp =  models.CharField(max_length=50)
    portfolio_url = models.CharField(max_length=255, default='not-set')
