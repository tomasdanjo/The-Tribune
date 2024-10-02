from django.shortcuts import render, get_object_or_404
from .models import Article

def landing_page(request):
    articles = Article.objects.all()
    return render(request, 'landing_page.html', {'articles': articles})

def full_article(request, id):
    article = get_object_or_404(Article,id=id)
    return render(request,'full_article_view.html',{'article':article})

