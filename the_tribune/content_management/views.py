from django.shortcuts import render, redirect, get_object_or_404
from .forms import Article_Form, Photo_Form, Tag_Form
from user_authentication.models import UserProfile
from article.models import Tag, Article
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ProfilePictureForm,ProfileBiographyForm
from datetime import datetime
from django.template.loader import render_to_string
from .models import Feedback
import json
from django.db.models import Q
from notification.models import *
from notification.views import create_notification



def tag_search_view(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    articles = Article.objects.filter(tag=tag, status='published').order_by('-date_published')

    return render(request, 'tag-search.html', {'tag': tag, 'articles': articles})

# from django import form


# Create your views here.
def writer_dashboard_view(request):
    articles = Article.objects.filter(writer = request.user.userprofile).order_by('-date_published')
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    submitted = articles.filter(status='submitted')
    archived = articles.filter(status='archived')
    current_date = datetime.now().strftime('%b %d, %Y')

    published = render_to_string('category-article-card.html',{'articles':published},request=request)
    drafts = render_to_string('category-article-card.html',{'articles':drafts},request=request)
    submitted = render_to_string('category-article-card.html',{'articles':submitted},request=request)
    archived = render_to_string('category-article-card.html',{'articles':archived},request=request)

    notifications = Notification.objects.all().filter(user=request.user).order_by('-created_at')

    unread_notifs = notifications.filter(is_read=False)
    read_notifs = notifications.filter(is_read=True)

    context = {
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'submitted':submitted,
        'archived':archived,
        'current_date':current_date,
        'show_search':True,
        'unread_notifs':unread_notifs,
        'read_notifs':read_notifs

    }

    print("iswriter ",request.user.userprofile.is_writer)


    return render(request,'writer_dashboard.html',context)

def editor_dashboard_view(request):

    articles = Article.objects.filter(editor=request.user.userprofile).order_by('-date_published')
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    archived = articles.filter(status='archived')
    review = articles.filter(status='submitted')
    
    current_date = datetime.now().strftime('%b %d, %Y')

    published = render_to_string('category-article-card.html',{'articles':published},request=request)
    drafts = render_to_string('category-article-card.html',{'articles':drafts},request=request)
    archived = render_to_string('category-article-card.html',{'articles':archived},request=request)
    review = render_to_string('category-article-card.html',{'articles':review},request=request)

    notifications = Notification.objects.all().filter(user=request.user).order_by('created_at')

    unread_notifs = notifications.filter(is_read=False)
    read_notifs = notifications.filter(is_read=True)

    context = {
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'archived':archived,
        'review':review,
        'current_date':current_date,
        'show_search':True,
        'unread_notifs':unread_notifs,
        'read_notifs':read_notifs

    }

    return render(request,'editor_dashboard.html',context)



def create_article(request):
    editors = UserProfile.objects.filter(is_editor=True)
    writer = UserProfile.objects.get(user_credentials=request.user)
    current_date = datetime.now().strftime('%b %d, %Y')

    if request.method == 'POST':
        article_form = Article_Form(request.POST)
        photo_form = Photo_Form(request.POST, request.FILES)  # Make sure FILES is included
        tag_form = Tag_Form(request.POST)

        # Log the request data for debugging
        print(request.POST)
        print(request.FILES)

        if article_form.is_valid() and photo_form.is_valid() and tag_form.is_valid():
            # Save the Photo
            photo = photo_form.save()

            # Handle the Tag creation
            tag_name = tag_form.cleaned_data['tag_name']
            existing_tag = Tag.objects.filter(tag_name=tag_name).first()

            if existing_tag:
                tag = existing_tag
            else:
                tag = tag_form.save()  # Save new tag

            # Create the Article object
            article = article_form.save(commit=False)
            article.writer = writer
            article.photo = photo
            article.tag = tag

            # Get the selected editor from the form
            editor_id = request.POST.get('editor')
            print(editor_id)
            if editor_id:
                editor = UserProfile.objects.get(pk=editor_id)
                article.editor = editor
            else:
                article.editor = writer

            # Set the article status based on the action
            action = request.POST.get('action')
            if action == "save_draft":
                article.status = "draft"
                article.save()

                notif_title = "Article Saved as Draft"
                notif_message = f"New article '{article.headline}' saved as draft."
                link = f"/draft/{article.id}"
                notification_type = "draft"  # Example notification type
                create_notification(writer.user_credentials, notif_title, notif_message, notification_type,link)


            elif action == "submit_review":
                article.status = "submitted"
                article.save()

                notif_title = "Article Submitted for Review"
                notif_message = f"New article '{article.headline}' has been submitted for review."
                link = f"/approve_article/{article.id}"
                notification_type = "review"  # Example notification type
                create_notification(writer.user_credentials, notif_title, notif_message, notification_type,link)

                
            elif action == "publish":
                article.status = "published"
                article.save()
                
                notif_title = "Article Published"
                notif_message = f"Your article '{article.headline}' has been published! Click to view."
                link = f"/article/{article.id}"
                notification_type = "publish"  # Example notification type
                create_notification(writer.user_credentials, notif_title, notif_message,notification_type , link)


                notif_title = "Article Published"
                notif_message = f"You have published the article '{article.headline}'. Click to view."
                
                notification_type = "publish" 
                editor=article.editor 
                create_notification(editor.user_credentials, notif_title, notif_message,notification_type ,link )


                

              # Save the article
      

            # Redirect based on user role
            if writer.is_writer:
                return redirect('writer_dashboard')
            elif writer.is_editor:
                return redirect('editor_dashboard')
        else:
            # Print errors for debugging
            print(article_form.errors)
            print(photo_form.errors)
            print(tag_form.errors)

    else:
        article_form = Article_Form()
        photo_form = Photo_Form()
        tag_form = Tag_Form()

    return render(request, 'create_article.html', {
        'article_form': article_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'editors': editors,
        'writer': writer,
        'current_date':current_date
    })

def draft_article(request,id):
    article = get_object_or_404(Article,id=id)
    current_date = datetime.now().strftime('%b %d, %Y')

    context = {
        'article':article,
        'current_date':current_date,
        'show_search':False
    }
    
    return render(request,'draft-article.html',context)

def edit_article(request, id):
    article = get_object_or_404(Article, id=id)
    editors = UserProfile.objects.filter(is_editor=True)
    writer = UserProfile.objects.get(user_credentials=request.user)
    current_date = datetime.now().strftime('%b %d, %Y')

    if request.method == 'POST':
        article_form = Article_Form(request.POST, instance=article)
        photo_form = Photo_Form(request.POST, request.FILES, instance=article.photo)
        tag_form = Tag_Form(request.POST, instance=article.tag)

        if article_form.is_valid() and photo_form.is_valid() and tag_form.is_valid():
            photo = photo_form.save()
            article = article_form.save(commit=False)
            article.writer = writer
            article.photo = photo
            article.tag = tag_form.save()

            editor_id = request.POST.get('editor')

            if editor_id:
                article.editor = UserProfile.objects.get(pk=editor_id)
            else:
                article.editor = writer

            action = request.POST.get('action')
            article.status = "draft" if action == "save_draft" else "submitted" if action == "submit_review" or action=="save" else "published"
            article.save()

            notif_title = "Article Edited"
            notif_message = f"You have edited the article '{article.headline}'. View Changes."
            link = f"/draft/{article.id}"
            notification_type = "article_edit"  # Example notification type
            create_notification(request.user, notif_title, notif_message,  notification_type,link)


            return redirect('writer_dashboard' if writer.is_writer else 'editor_dashboard')

    else:
        article_form = Article_Form(instance=article)
        photo_form = Photo_Form(instance=article.photo)
        tag_form = Tag_Form(instance=article.tag)
        photo_instance=article.photo
    
    print(article.status)

    return render(request, 'create_article.html', {
        'article':article,
        'article_form': article_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'editors': editors,
        'writer': writer,
        'selected_editor': article.editor.id if article.editor else None, 
        'photo_instance':photo_instance,
        'current_date':current_date
    })


def approve_article(request,id):
    article = get_object_or_404(Article,id=id)
    current_date = datetime.now().strftime('%b %d, %Y')

    feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain the ordering by date within each status group
            )
    
    context = {
        'article':article,
        'current_date':current_date,
        'feedbacks':feedbacks
    }
    return render(request,'approve-article.html',context)

def archive_view(request,id):
    article = get_object_or_404(Article,id=id)
    feedbacks = Feedback.objects.filter(article=article)[:1]
    current_date = datetime.now().strftime('%b %d, %Y')

    context = {
        'article':article,
        'feedbacks':feedbacks,
        'current_date':current_date,
        'show_search':True,
    }

    return render(request,'archive-view.html',context)

def archive_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    writer = article.writer

    if request.method == 'POST':
        archive_reason = request.POST.get('archive_reason')
        if archive_reason:
            Feedback.objects.create(
                article=article,
                editor=request.user.userprofile,  # Assuming the user has a UserProfile
                comment=archive_reason,
                status='resolved'
            )

            # Update the article status to 'archived'
            article.status = 'archived'
            article.save()

            notif_title = "Article Archived"
            notif_message = f"Your article '{article.headline}' has been archived. View the editor's feedback."
            link = f"/archive/{article.id}"
            notification_type = "archive"  # Example notification type
            create_notification(writer.user_credentials, notif_title, notif_message,notification_type, link )

            notif_title = "Article Archived"
            notif_message = f"You have archived the article '{article.headline}'."
            link = f"/archive/{article.id}"
            notification_type = "archive"  # Example notification type
            create_notification(request.user, notif_title, notif_message, notification_type,link )

            

            messages.success(request, 'Article archived with feedback.')
            return redirect('editor_dashboard')
        else:
            messages.error(request, 'Please provide a reason for archiving.')
            return redirect('editor_dashboard')
    return redirect('editor_dashboard')


def publish_article(request, id):
    article = get_object_or_404(Article, id=id)
    writer = article.writer
    article.status = 'published'
    article.save()

    notif_title = "Article Published"
    notif_message = f"Your article '{article.headline}' has been published! Click to view."
    link = f"/article/{article.id}"
    notification_type = "publish"  # Example notification type
    create_notification(writer.user_credentials, notif_title, notif_message, notification_type,link )





    return redirect('editor_dashboard') 


@csrf_exempt  # Use this decorator if needed, or include CSRF middleware for this view
def submit_feedback(request, article_id):
    if request.method == 'POST':
        article_id = article_id
        feedback_text = request.POST.get('feedback')

        if article_id and feedback_text:
            article = Article.objects.get(id=article_id)
            editor = request.user.userprofile
            feedback = Feedback.objects.create(article=article, editor=editor, comment=feedback_text)
            feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain the ordering by date within each status group
            ) # Fetch all feedbacks

            writer=article.writer

            notif_title = "Article Feedback"
            notif_message = f"{feedback.editor}: \"{feedback.comment}\" View article feedback"
            link = f"/approve_article/{article.id}/"
            notification_type = "feedback"  # Example notification type
            create_notification(writer.user_credentials, notif_title, notif_message, notification_type,link)


            # Render the feedback template as a string
            feedback_html = render_to_string('feedback-template.html',{'feedbacks': feedbacks,},request=request)
            return JsonResponse({'status': 'success','feedback_html':feedback_html})

        return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def delete_draft(request, article_id):

    article = get_object_or_404(Article, id=article_id)
    
    if request.method == 'POST':
        article.delete()
        return redirect('editor_dashboard')  
    return redirect('editor_dashboard')

def update_profile(request,id):
    # Get the user profile for the currently logged-in user
    profile = get_object_or_404(UserProfile,id=id)
    # If the request method is POST, we want to handle the form submission
    if request.method == 'POST':
        pictureform = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        biographyform = ProfileBiographyForm(request.POST,instance=profile)

        if pictureform.is_valid():
            pictureform.save()  
        if biographyform.is_valid():
            biographyform.save()


        notif_title = "Profile Update"
        notif_message = "You have successfully updated your profile. Click to view changes."
        link = f"/view_profile/{profile.id}"
        notification_type = "profile"  # Example notification type
        create_notification(profile.user_credentials,notif_title,notif_message,notification_type,link)


        if profile.is_editor:
                return redirect('editor_dashboard')  # Redirect
        elif profile.is_writer:
                return redirect('writer_dashboard')  # Redirect
    else:
        # GET request, so pre-fill the form with the current profile picture
        pictureform = ProfilePictureForm(instance=profile)
        biographyform = ProfileBiographyForm(instance=profile)
    # Render the template with the form
    current_date = datetime.now().strftime('%b %d, %Y') 
    context = {
        'pictureform': pictureform,
        'biographyform':biographyform, 
        'profile': profile,
        'current_date':current_date
    }
    return render(request, 'update_profile_picture.html', context)

def tag_search_view(request):
    query = request.GET.get('search', '')
    if query:
        tags = Tag.objects.filter(tag_name__icontains=query)
        articles = Article.objects.filter(tag__in=tags)
    else:
        tags = Tag.objects.all() 
        articles = Article.objects.none()  

    return render(request, 'tag-search.html', {'tags': tags, 'articles': articles, 'query': query})


def filter_feedbacks(request, id):

    if request.method == "POST":
        article = get_object_or_404(Article, id=id)
        status = request.POST.get("status")

        if status == "show-all":
            feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain the ordering by date within each status group
            ) # Fetch all feedbacks
        else:
            feedbacks = Feedback.objects.filter(article=article, status=status)  # Filter by status

        feedback_html = render_to_string(
            "feedback-template.html", {"feedbacks": feedbacks,}, request=request
        )
        return JsonResponse({"status": "success", "feedback_html": feedback_html})

    return JsonResponse({"status": "error", "message": "Invalid request method"})

    
def resolve_feedback(request, feedback_id):

    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.status = 'resolved'
        feedback.save()

        article = feedback.article

        notif = f"Your feedback \"{feedback.comment}\" on article \"{article.headline}\" has been resolved. Click to view."
        link = f"/approve_article/{article.id}/" 
        create_notification(feedback.editor.user_credentials,notif,link)

        # Fetch all feedbacks related to the article
        article = feedback.article
        selected_status = request.POST.get("status", "show-all")

        if selected_status == "show-all":
            feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain ordering by date within each status group
            )
        else:
            feedbacks = Feedback.objects.filter(article=article, status=selected_status).order_by('-created_at')


        # Render the updated feedback list
        feedback_html = render_to_string(
            'feedback-template.html',
            {'feedbacks': feedbacks,},
            request=request
        )
        return JsonResponse({'status': 'success', 'feedback_html': feedback_html})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_feedback(request, feedback_id):

    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        article=feedback.article

        # Create the notification details
        notif_title = "Feedback Deleted"
        notif_message = f"Your feedback \"{feedback.comment}\" on article \"{article.headline}\" has been deleted. Click to view article."
        link = f"/approve_article/{article.id}/"
        notification_type = "feedback"  # Example notification type

        # Create the notification for the editor
        create_notification(feedback.editor.user_credentials, notif_title, notif_message, notification_type, link)



        feedback.delete()

        # Fetch all feedbacks related to the article
        article = feedback.article
        selected_status = request.POST.get("status", "show-all")

        if selected_status == "show-all":
            feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain ordering by date within each status group
            )
        else:
            feedbacks = Feedback.objects.filter(article=article, status=selected_status).order_by('-created_at')


        # Render the updated feedback list
        feedback_html = render_to_string(
            'feedback-template.html',
            {'feedbacks': feedbacks,},
            request=request
        )
        return JsonResponse({'status': 'success', 'feedback_html': feedback_html})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def update_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        data = json.loads(request.body)
        feedback.comment = data.get("comment", feedback.comment)
        article = feedback.article

        # Create the notification details
        notif_title = "Feedback Updated"
        notif_message = f"Your feedback \"{feedback.comment}\" on article \"{article.headline}\" has been updated. Click to view article."
        link = f"/approve_article/{article.id}/"
        notification_type = "feedback"  # Example notification type

        # Create the notification for the editor
        create_notification(feedback.editor.user_credentials, notif_title, notif_message, notification_type, link)



        feedback.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)




@csrf_exempt  # Use CSRF token in production for security
def add_reply(request, feedback_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        reply_text = data.get('reply')

        if not reply_text:
            return JsonResponse({'success': False, 'error': 'Reply text is required'}, status=400)
        author=request.user.userprofile
        feedback = Feedback.objects.get(id=feedback_id)
        reply = Reply.objects.create(
            feedback=feedback,
            author=author,  # Assuming the user is authenticated
            reply=reply_text
        )
        article = feedback.article
        # Create the notification details
        notif_title = "New Reply to Your Feedback"
        notif_message = f"{author.first_name} {author.last_name} replied \"{reply_text}\" to your feedback \"{feedback.comment}\" on article \"{article.headline}.\" Click to view."
        link = f"/approve_article/{article.id}/"
        notification_type = "reply_to_feedback"  # Example notification type

        # Create the notification for the editor
        create_notification(feedback.editor.user_credentials, notif_title, notif_message, notification_type, link)


        # Retrieve all replies for the feedback to update the UI
        replies = Reply.objects.filter(feedback=feedback)
        replies_html = render_to_string('replies-template.html', {'replies': replies,},request=request)

        response_data = {
            'success': True,
            'replies_html': replies_html,
        }
        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)

@csrf_exempt  # Remove this decorator if you want CSRF protection
def update_reply(request, reply_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        updated_reply_text = data.get('reply')

        if not updated_reply_text:
            return JsonResponse({'success': False, 'error': 'Reply text is required'}, status=400)

        try:
            reply = Reply.objects.get(id=reply_id)
            # Ensure the current user is allowed to edit this reply
            if request.user == reply.author.user_credentials:
                reply.reply = updated_reply_text

                author = reply.author
                feedback = reply.feedback
                article = feedback.article
                # Create the notification details
                notif_title = "Reply Edited"
                notif_message = f"{author.first_name} {author.last_name} has edited their reply on your feedback \"{feedback.comment}\" on article \"{article.headline}.\" Click to view."
                link = f"/approve_article/{article.id}/"
                notification_type = "reply"  # Example notification type

                # Create the notification for the editor
                create_notification(feedback.editor.user_credentials, notif_title, notif_message, notification_type, link)



                reply.save()
                return JsonResponse({'success': True, 'reply': updated_reply_text})
            else:
                return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
        except Reply.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Reply not found'}, status=404)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)


def delete_reply(request, reply_id):
    if request.method == "POST":
        try:
            reply = Reply.objects.get(id=reply_id)
           # Create the notification details
            notif_title = "Reply Deleted"
            notif_message = f"Your reply \"{reply.reply}\" on feedback \"{reply.feedback.comment}\" on article \"{reply.feedback.article.headline}\" has been deleted."
            notification_type = "reply"  # Example notification type

            # Create the notification for the author of the reply
            create_notification(reply.author.user_credentials, notif_title, notif_message, notification_type)



            reply.delete()
            return JsonResponse({"status": "success"})  # Match "status" with your JS logic
        except Reply.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Reply not found."})
    return JsonResponse({"status": "error", "message": "Invalid request method."})


def view_profile(request, id):
    # Fetch published articles authored by the user
    profile = UserProfile.objects.get(id=id)


    articles = Article.objects.filter(
    Q(writer=profile) | Q(editor=profile), 
    status='published').order_by('-date_published')

    current_date = datetime.now().strftime('%b %d, %Y')
    published_articles = articles.filter(status='published')

    context = {
        'profile':profile,
        'articles': published_articles,
        'current_date':current_date,
        'show_search':True
    }

    return render(request, 'view_profile.html', context)

# In views.py
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def mark_notification_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)

def get_unread_notifications(request):
    # Fetch read notifications from your database
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
    
    # Render the notifications with the 'notification-card.html' template
    return render(request, 'notification-card.html', {'notifications': unread_notifications})

def get_read_notifications(request):
    # Fetch read notifications from your database
    read_notifications = Notification.objects.filter(user=request.user, is_read=True).order_by('-created_at')
    
    # Render the notifications with the 'notification-card.html' template
    return render(request, 'notification-card.html', {'notifications': read_notifications})
    

@csrf_exempt  # Remove this decorator in production and use proper CSRF protection
def mark_as_read(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        notification_id = data.get('id')
        
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = True  # Assuming there's an 'is_read' field
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@csrf_exempt  # Remove this decorator in production and use proper CSRF protection
def mark_as_unread(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        notification_id = data.get('id')
        
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.is_read = False  # Assuming there's an 'is_read' field
            notification.save()
            return JsonResponse({'success': True})
        except Notification.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Notification not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})
