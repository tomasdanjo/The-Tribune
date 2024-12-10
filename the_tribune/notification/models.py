from django.db import models
from user_authentication.models import UserProfile, User

# Create your models here.
class Notification(models.Model):
  NOTIFICATION_TYPES = [
        ('article', 'Article'),
        ('feedback', 'Feedback'),
        ('profile', 'Profile'),
        ('draft','Draft'),
        ('review','Review'),
        ('publish','Publish'),
        ('article_edit','Article Edited'),
        ('archive','Archive'),
        ('reply','Reply to Feedback'),

  ]  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  title = models.CharField(max_length=255)  
  notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
  link = models.URLField(blank=True, null=True)  # Optional link for redirection
    
  def __str__(self):
    return f"Notification for {self.user.username}"
  

