from django.urls import path

from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('writer_dashboard/',writer_dashboard_view,name='writer_dashboard'),
    path('editor_dashboard/',editor_dashboard_view,name='editor_dashboard'),
    path('create_article/',create_article, name='create_article'),
    path('draft/<int:id>/',draft_article, name='draft'),
    path('edit_article/<int:id>/',edit_article, name='edit_article'),
    path('approve_article/<int:id>/',approve_article, name='approve'),
    path('articles/<int:article_id>/archive/', archive_article, name='archive_article'),
    path('archive/<int:id>', archive_view, name='archive'),
    path('publish_article/<int:id>', publish_article, name='publish_article'),
    path('submit-feedback/', submit_feedback, name='submit_feedback'),
    path('editor_dashboard/<int:article_id>/', delete_draft, name='delete_draft'),
    path('update_profile/<int:id>',update_profile, name='update_profile'),
    path('view_profile/<int:id>',view_profile, name='view_profile'),
    path('tags/', tag_search_view, name='tag-search'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)