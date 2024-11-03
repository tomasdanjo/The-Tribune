from django.db import models
from article.models import Article
from user_authentication.models import UserProfile


# Create your models here.
class Feedback(models.Model):
  article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='feedbacks')
  editor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='feedbacks')
  
  comment = models.TextField()

  created_at = models.DateTimeField(auto_now_add=True)

  STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
  ]

  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

  class Meta:
      ordering = ['-created_at']  # Sort feedback by latest first

  def __str__(self):
      return f"Feedback for Article ID {self.article.id} by {self.user.username if self.user else 'Anonymous'}"