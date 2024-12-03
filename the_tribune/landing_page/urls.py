from django.urls import path
from .views import *


urlpatterns = [
    path('',landing_page,name='home'),
    path('article/<int:id>/',full_article,name='full_article_view'),
    path('subscribe/', subscribe, name='subscribe'),
    path('add_comment/<int:article_id>/', add_comment, name='add_comment'),
    path('like-comment/', like_comment, name='like_comment'),
    path('dislike-comment/', dislike_comment, name='dislike_comment'),
    path('articles/<int:article_id>/sort_comments/', sort_comments, name='sort_comments'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
     path('load-more-comments/<int:article_id>/<int:offset>/', load_more_comments, name='load_all_comments'),
]