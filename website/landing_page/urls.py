from django.urls import path
from .views import landing_page, full_article, search_article

urlpatterns = [
    path('',landing_page,name='home'),
    path('article/<int:id>/',full_article,name='full_article_view'),
    path('search/',search_article,name='search')
    # path('article_detail/',landing_page,name="article_view")
]