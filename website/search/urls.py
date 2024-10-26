from django.urls import path
from .views import search_article

urlpatterns = [
    path('search/',search_article,name='search')
    # path('article_detail/',landing_page,name="article_view")
]