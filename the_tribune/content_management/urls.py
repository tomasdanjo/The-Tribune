from django.urls import path
from .views import writer_dashboard_view, create_article, editor_dashboard_view,edit_article
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('writer_dashboard/',writer_dashboard_view,name='writer_dashboard'),
    path('editor_dashboard/',editor_dashboard_view,name='editor_dashboard'),
    
    path('create_article/',create_article, name='create_article'),
    path('edit_article/<int:article_id>/',edit_article,name='edit_article_view'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)