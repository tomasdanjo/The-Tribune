from django.shortcuts import render
from .models import *

# Create your views here.
def create_notification(user, title, message, notification_type,link=None):
    Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link,
        notification_type=notification_type,
    )