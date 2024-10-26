from django.urls import path

from .views import writer_dashboard_view, create_article, editor_dashboard_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('writer_dashboard/',writer_dashboard_view,name='writer_dashboard'),
    path('editor_dashboard/',editor_dashboard_view,name='editor_dashboard'),
    
    path('create_article/',create_article, name='create_article'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)