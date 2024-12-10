from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import ArticleAnalytics
from landing_page.models import Comment


@receiver(post_save, sender=Comment)
def update_comment_count_on_save(sender, instance, created, **kwargs):
    if instance.article.status == 'published':
        today = timezone.now().date()
        analytics, _ = ArticleAnalytics.objects.get_or_create(
            article=instance.article, 
            date=today,
            defaults={'views': 0, 'comments': 1, 'shares': 0}
        )
        
        if created:
            analytics.comments += 1
            analytics.save()


@receiver(post_save, sender=Comment)
def update_comment_analytics(sender, instance, created, **kwargs):
    """
    Update comment count in ArticleAnalytics when a new comment is added
    """
    if created and instance.article.status == 'published':
        today = timezone.now().date()
        
        # Get or create daily analytics for the article
        analytics, _ = ArticleAnalytics.objects.get_or_create(
            article=instance.article, 
            date=today,
            defaults={'views': 0, 'comments': 1, 'shares': 0}
        )
        
        # Increment comments
        analytics.comments += 1
        analytics.save()