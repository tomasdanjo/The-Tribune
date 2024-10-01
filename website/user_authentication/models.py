from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
        
    ROLE_CHOICES = [
        ('writer', 'Writer'),
        ('editor', 'Editor'),
        ('user', 'User'),
        ('admid', 'Admin'),
    ]
        
    user_credentials = models.OneToOneField(User,on_delete=models.CASCADE)
    #defaul 2006
    birthdate = models.DateField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user_credentials.username