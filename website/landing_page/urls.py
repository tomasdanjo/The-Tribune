from django.urls import path
from .views import landing_page

urlpatterns = [
    # path('signup/',signup,name='signup'),
    # path('login/',login,name='login')
    path('',landing_page,name='home'),
]