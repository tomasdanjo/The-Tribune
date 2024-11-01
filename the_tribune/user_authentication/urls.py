from django.urls import path
from .views import login_view, signup_view, signup_user_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/',signup_view,name='signup'),
    path('login/',login_view,name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signupuser',signup_user_view,name='signup_user')
]