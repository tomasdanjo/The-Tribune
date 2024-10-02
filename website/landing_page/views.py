from django.shortcuts import render
from .models import Article

def landing_page(request):
    articles = Article.objects.all()
    return render(request, 'landing_page.html', {'articles': articles})
