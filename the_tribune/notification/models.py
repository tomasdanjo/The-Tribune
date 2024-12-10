from django.db import models
from user_authentication.models import UserProfile

# Create your models here.
class Notification(models.Model):
  user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  message = models.TextField()
  is_read = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  link = models.URLField(blank=True, null=True)  # Optional link for redirection
    
  def __str__(self):
    return f"Notification for {self.user.username}"