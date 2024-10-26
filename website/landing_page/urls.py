from django.urls import path
from .views import landing_page, full_article
urlpatterns = [
    path('',landing_page,name='home'),
    path('article/<int:id>/',full_article,name='full_article_view'),
]