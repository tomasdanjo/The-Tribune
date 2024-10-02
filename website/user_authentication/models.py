from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
        
    ROLE_CHOICES = [
        ('writer', 'Writer'),
        ('editor', 'Editor'),
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
        
    user_credentials = models.OneToOneField(User,on_delete=models.CASCADE)
    #defaul 2006
    birthdate = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user_credentials.username
    

class Notification(models.Model):
    message = models.TextField()
    date_notified = models.DateTimeField()
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    
    