from django.db import models
from user_authentication.models import UserProfile
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'News'),
        ('sports', 'Sports'),
        ('religion', 'Religion'),
        ('entertainment', 'Entertainment'),
        ('technology', 'Technology'),
        ('lifestyle', 'Lifestyle'),
        ('opinion','Opinion'),
        ('editorial','Editorial'),
        ('featured_topics','Featured Topics'),
        ('environment','Environment'),
        ('sci_and_tech','Science & Tech.')
        

    ]

    category_name = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='news')


    def __str__(self):
        return self.get_category_name_display()  # To display the readable name


class Photo(models.Model):
    photo = models.ImageField(upload_to='article_photos/')
    caption = models.CharField(max_length=200)
    date_taken = models.DateField()

    

class Tag(models.Model):
    tag_name = models.CharField(max_length=100) 

class Article(models.Model):
    STATUS_CHOICES = [
    ('draft', 'Draft'),  # When the writer first creates the article
    ('submitted', 'Submitted for Review'),  # When the writer submits for editor review
    ('in_review', 'In Review'),  # When the editor is reviewing the article
    ('rejected', 'Rejected'),  # When the editor rejects the article
    ('revision', 'Under Revision'),  # When the article is being revised by the writer after rejection
    ('archived', 'Archived'),  # When the article is permanently archived
    ('published', 'Published')  # When the article is approved and published by the editor
    ]
  
    headline = models.CharField(max_length=255)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='draft')  # This is the correct status field
    date_published = models.DateTimeField(auto_now=True)
    writer = models.ForeignKey(UserProfile, on_delete=models.RESTRICT, related_name="writer")
    editor = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING, related_name="editor")
    photo = models.ForeignKey(Photo, on_delete=models.RESTRICT)
    tag = models.ForeignKey(Tag, on_delete=models.RESTRICT)
    category = models.ForeignKey('Category', on_delete=models.RESTRICT, default=1)

class ArticleAnalytics(models.Model):
    article = models.ForeignKey(Article, related_name='analytics', on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    views = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)

    class Meta:
        unique_together = ('article', 'date')
        ordering = ['date']
