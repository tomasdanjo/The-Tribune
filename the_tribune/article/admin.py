from django.contrib import admin
from .models import Category,Photo,Tag,Article,ArticleAnalytics

# Register your models here.
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(ArticleAnalytics)