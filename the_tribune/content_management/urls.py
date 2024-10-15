from django.urls import path
from .views import writer_dashboard_view

urlpatterns = [
    path('writer-dashboard/',writer_dashboard_view,name='writer-dashboard'),
    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard')
]