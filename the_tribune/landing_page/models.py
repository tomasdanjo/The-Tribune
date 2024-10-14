from django.db import models
from article.models import Article
from user_authentication.models import UserProfile

# Create your models here.
class Comment(models.Model):
  article_id  = models.ForeignKey(Article,on_delete=models.CASCADE)
  commenter_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  date_published = models.DateTimeField(auto_now_add=True)
  content = models.TextField()
  liked_by = models.ManyToManyField(UserProfile, related_name="liked_comments", blank=True)

  def __str__(self):
    return self.content