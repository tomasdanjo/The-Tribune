from django.shortcuts import render


# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Article, ArticleAnalytics

class ArticleAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    
    @action(detail=True, methods=['GET'])
    def get_analytics(self, request, pk=None):
        article = self.get_object()
        analytics = ArticleAnalytics.objects.filter(article=article)
        
        return Response({
            'analytics': [
                {
                    'date': entry.date.isoformat(),
                    'views': entry.views,
                    'comments': entry.comments,
                    'shares': entry.shares
                } for entry in analytics
            ]
        })
    
from django.shortcuts import render, get_object_or_404
from .models import Article, ArticleAnalytics
from django.db.models import Sum
import json
from datetime import datetime

def article_analytics_view(request, article_id):
    # Get the specific article
    article = get_object_or_404(Article, id=article_id)
    articles = [article] 

    
    # Fetch the analytics for this article, ordered by date
    analytics = ArticleAnalytics.objects.filter(article=article).order_by('date')
    
    # Prepare data for Chart.js
    dates = [entry.date.strftime('%Y-%m-%d') for entry in analytics]
    views = [entry.views for entry in analytics]
    comments = [entry.comments for entry in analytics]
    shares = [entry.shares for entry in analytics]
    
    current_date = datetime.now().strftime('%b %d, %Y')
    
    # Convert data to JSON for JavaScript
    context = {
        'articles':articles,
        'article': article,
        'dates_json': json.dumps(dates),
        'views_json': json.dumps(views),
        'comments_json': json.dumps(comments),
        'shares_json': json.dumps(shares),
        'current_date':current_date,
        'show_search':True
    }
    
    return render(request, 'article-analytics.html', context)