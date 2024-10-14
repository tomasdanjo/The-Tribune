from django.shortcuts import render

from article.models import Article


def search_article(request):
    query = request.GET.get('query')
    articles = Article.objects.filter(headline__icontains=query)  # Adjust as necessary for your search logic
    return render(request, 'search_results.html', {'articles': articles})