from django.contrib import admin
from .models import Comment, Subscription

# Register your models here.
admin.site.register(Comment)
admin.site.register(Subscription)