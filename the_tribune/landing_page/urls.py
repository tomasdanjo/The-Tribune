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
    path('view_profile/<int:id>',view_profile, name='view_profile'),
    path('summarize/<int:article_id>/', summarize_article, name='summarize_article'),
    path('about-us/', about_us, name='about_us'),
    path('mission/', mission_statement, name='mission_statement'),
    path('ai-guidelines/', ai_guidelines, name='ai_guidelines'),
    path('the-team/', the_team, name='the_team'),
    path('job-opening/', job_openings, name='job_openings'),
    path('contact-us/', contact_us, name='contact_us'),
    path('category/<int:id>/',category_view, name='category_view'),
    path('tag/<int:id>/',tag_view, name='tag_view'),
]