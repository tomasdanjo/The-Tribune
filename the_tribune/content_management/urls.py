from django.urls import path
from .views import writer_dashboard_view, create_article

urlpatterns = [
    path('writer_dashboard/',writer_dashboard_view,name='writer_dashboard'),
    path('create_article/',create_article, name='create_article'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard')
]