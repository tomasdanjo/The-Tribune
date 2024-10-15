from django.shortcuts import render,get_object_or_404
from article.models import Article
from .models import Comment
from django.utils import timezone
# from myapp.models import Article

def landing_page(request):
    articles = Article.objects.all()
    for article in articles:
        if timezone.is_naive(article.date_published):
            article.date_published = timezone.make_aware(article.date_published, timezone.get_current_timezone())
            article.save()
            
    return render(request, 'landing_page.html', {'articles': articles})

def full_article(request, id):
    article = get_object_or_404(Article,id=id)
    comments = Comment.objects.filter(article_id=id)
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id)
    

    return render(request,'full_article_view.html',{'article':article,'comments':comments,'related_stories':related_stories})

