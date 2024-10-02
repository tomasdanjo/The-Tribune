from django.db import models

from user_authentication.models import UserProfile

# Create your models here.
class Category(models.Model):
  category_name = models.CharField(max_length=100)
  
class Photo(models.Model):
  photo = models.ImageField(upload_to='article_photos/')
  caption = models.CharField(max_length=200)
  date_taken = models.DateField()

class Tag(models.Model):
  tag_name = models.CharField(max_length=100)

class Article(models.Model):
  headline = models.CharField(max_length=255)
  content = models.TextField()
  date_created = models.DateTimeField()
  status = models.CharField(max_length=100)
  date_published = models.DateTimeField()
  writer_id = models.ForeignKey(UserProfile, on_delete=models.RESTRICT,related_name="writer_id")
  editor_id = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING,related_name="editor_id")
  photo_id = models.ForeignKey(Photo, on_delete=models.RESTRICT)
  tag_id = models.ForeignKey(Tag, on_delete=models.RESTRICT)



class Comment(models.Model):
  article_id  = models.ForeignKey(Article,on_delete=models.DO_NOTHING)
  commenter_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
  date_published = models.DateTimeField()
  content = models.TextField()






