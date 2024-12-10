from django.urls import path

from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('writer_dashboard/',writer_dashboard_view,name='writer_dashboard'),
    path('editor_dashboard/',editor_dashboard_view,name='editor_dashboard'),
    path('create_article/',create_article, name='create_article'),
    path('draft/<int:id>/',draft_article, name='draft'),
    path('edit_article/<int:id>/',edit_article, name='edit_article'),
    path('approve_article/<int:id>/',approve_article, name='approve'),
    path('articles/<int:article_id>/archive/', archive_article, name='archive_article'),
    path('archive/<int:id>', archive_view, name='archive'),
    path('publish_article/<int:id>', publish_article, name='publish_article'),
    path('submit_feedback/<int:article_id>/', submit_feedback, name='submit_feedback'),
    path('editor_dashboard/<int:article_id>/', delete_draft, name='delete_draft'),
    path('update_profile/<int:id>',update_profile, name='update_profile'),
    path('view_profile/<int:id>',view_profile, name='view_profile'),
    path('filter_feedbacks/<int:id>/',filter_feedbacks, name='filter_feedbacks'),
    path('resolve_feedback/<int:feedback_id>/', resolve_feedback, name='resolve_feedback'),
    path('delete_feedback/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
    path('feedback/update/<int:feedback_id>/', update_feedback, name='update_feedback'),
    path('reply/add/<int:feedback_id>/', add_reply, name='add_reply'),
    path('reply/update/<int:reply_id>/', update_reply, name='update_reply'),
    path('delete_reply/<int:reply_id>/', delete_reply, name='delete_reply'),
    path('notifications/mark_all_read/', mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/mark_read/<int:notification_id>/', mark_notification_read, name='mark_notification_read'),
    path('notifications/read/', get_read_notifications, name='get_read_notifications'),
    path('notifications/unread/', get_unread_notifications, name='get_unread_notifications'),
    path('mark-as-read/', mark_as_read, name='mark_as_read'),
    path('mark-as-unread/', mark_as_unread, name='mark_as_unread'),

    



    # path('editor-dashboard/',editor_dashboard_view,name='editor-dashboard'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)