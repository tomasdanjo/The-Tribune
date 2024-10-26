from django.contrib import admin

# Register your models here.
from .models import Comment, Photo, Article, Category, Tag

admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Article)
admin.site.register(Tag)


