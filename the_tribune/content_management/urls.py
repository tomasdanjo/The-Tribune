from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import writer_dashboard_view,writer_create_article,writer_dashboard_view_pending,writer_dashboard_view_rejected
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('writer-dashboard/',writer_dashboard_view,name='writer-dashboard'),
    path('writer-create-article/',writer_create_article,name='create'),
    path('writer_dashboard_view_pending/',writer_dashboard_view_pending,name='pending'),
    path('writer_dashboard_view_rejected/',writer_dashboard_view_rejected,name='rejected'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard')
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)