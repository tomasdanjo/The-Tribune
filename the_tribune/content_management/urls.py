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
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)