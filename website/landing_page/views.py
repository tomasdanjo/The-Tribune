from django.shortcuts import render, get_object_or_404
from .models import Article, Comment

def landing_page(request):
    articles = Article.objects.all()
    return render(request, 'landing_page.html', {'articles': articles})

def full_article(request, id):
    article = get_object_or_404(Article,id=id)
    comments = Comment.objects.filter(article_id=id)
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id)
    return render(request,'full_article_view.html',{'article':article,'comments':comments,'related_stories':related_stories})

def search_article(request):
    query = request.GET.get('query')
    articles = Article.objects.filter(headline__icontains=query)  # Adjust as necessary for your search logic
    return render(request, 'search_results.html', {'articles': articles})