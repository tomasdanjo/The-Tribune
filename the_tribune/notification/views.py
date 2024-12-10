from django.shortcuts import render
from .models import *

# Create your views here.
def create_notification(user, message, link=None):
    """
    Helper function to create notifications
    
    Args:
    - user: User to send notification to
    - message: Notification text
    - link: Optional URL to redirect when clicked
    """
    Notification.objects.create(
        user=user,
        message=message,
        link=link
    )