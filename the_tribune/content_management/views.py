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

# from django import form

# Create your views here.
def writer_dashboard_view(request):
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None
    articles = Article.objects.filter(writer = user)
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    submitted = articles.filter(status='submitted')
    archived = articles.filter(status='archived')
    current_date = datetime.now().strftime('%b %d, %Y')

    published = render_to_string('article-card.html',{'articles':published},request=request)
    drafts = render_to_string('article-card.html',{'articles':drafts},request=request)
    submitted = render_to_string('article-card.html',{'articles':submitted},request=request)
    archived = render_to_string('article-card.html',{'articles':archived},request=request)

    context = {
        'auth_user':user, 
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'submitted':submitted,
        'archived':archived,
        'current_date':current_date,
        'show_search':True

    }

    print("iswriter ",request.user.userprofile.is_writer)


    return render(request,'writer_dashboard.html',context)

def editor_dashboard_view(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user_credentials=request.user)
        except UserProfile.DoesNotExist:
            user = None

    articles = Article.objects.filter(editor=user)
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    archived = articles.filter(status='archived')
    review = articles.filter(status='submitted')
    
    current_date = datetime.now().strftime('%b %d, %Y')

    published = render_to_string('article-card.html',{'articles':published},request=request)
    drafts = render_to_string('article-card.html',{'articles':drafts},request=request)
    archived = render_to_string('article-card.html',{'articles':archived},request=request)
    review = render_to_string('article-card.html',{'articles':review},request=request)

    context = {
        'auth_user':user, 
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'archived':archived,
        'review':review,
        'current_date':current_date,
        'show_search':True

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
            elif action == "submit_review":
                article.status = "submitted"
            elif action == "publish":
                article.status = "published"

            article.save()  # Save the article

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
        'auth_user':writer,
        'current_date':current_date
    })

def draft_article(request,id):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user_credentials=request.user)
        except UserProfile.DoesNotExist:
            user = None
    article = get_object_or_404(Article,id=id)
    current_date = datetime.now().strftime('%b %d, %Y')

    context = {
        'article':article,
        'auth_user':user,
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
            article.status = "draft" if action == "save_draft" else "submitted" if action == "submit_review" else "published"
            article.save()

            return redirect('writer_dashboard' if writer.is_writer else 'editor_dashboard')

    else:
        article_form = Article_Form(instance=article)
        photo_form = Photo_Form(instance=article.photo)
        tag_form = Tag_Form(instance=article.tag)
        photo_instance=article.photo

    return render(request, 'create_article.html', {
        'article_form': article_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'editors': editors,
        'writer': writer,
        'selected_editor': article.editor.id if article.editor else None, 
        'auth_user':writer,
        'photo_instance':photo_instance,
        'current_date':current_date
    })


def approve_article(request,id):
    article = get_object_or_404(Article,id=id)
    current_date = datetime.now().strftime('%b %d, %Y')
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None


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
        'auth_user':user,
        'feedbacks':feedbacks
    }
    return render(request,'approve-article.html',context)

def archive_view(request,id):
    article = get_object_or_404(Article,id=id)
    feedback = Feedback.objects.filter(article=article)
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None
    
    current_date = datetime.now().strftime('%b %d, %Y')

    context = {
        'article':article,
        'feedback':feedback,
        'auth_user':user,
        'current_date':current_date,
        'show_search':True,
    }

    return render(request,'archive-view.html',context)

def archive_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)

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

            messages.success(request, 'Article archived with feedback.')
            return redirect('editor_dashboard')
        else:
            messages.error(request, 'Please provide a reason for archiving.')
            return redirect('editor_dashboard')
    return redirect('editor_dashboard')


def publish_article(request, id):
    article = get_object_or_404(Article, id=id)
    article.status = 'published'
    article.save()
    return redirect('editor_dashboard') 


@csrf_exempt  # Use this decorator if needed, or include CSRF middleware for this view
def submit_feedback(request, article_id):
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None
    if request.method == 'POST':
        article_id = article_id
        feedback_text = request.POST.get('feedback')

        if article_id and feedback_text:
            article = Article.objects.get(id=article_id)
            feedback = Feedback.objects.create(article=article, editor=request.user.userprofile, comment=feedback_text)
            feedbacks = Feedback.objects.filter(article=article).order_by(
                models.Case(
                    models.When(status='pending', then=0),
                    models.When(status='resolved', then=1),
                    default=2,
                ),
                '-created_at'  # Maintain the ordering by date within each status group
            ) # Fetch all feedbacks
        
            # Render the feedback template as a string
            feedback_html = render_to_string('feedback-template.html',{'feedbacks': feedbacks,'auth_user':user},request=request)
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
    user_profile = get_object_or_404(UserProfile,id=id)
    # If the request method is POST, we want to handle the form submission
    if request.method == 'POST':
        pictureform = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
        biographyform = ProfileBiographyForm(request.POST,instance=user_profile)

        if pictureform.is_valid():
            pictureform.save()  
        if biographyform.is_valid():
            biographyform.save()

        if user_profile.is_editor:
                return redirect('editor_dashboard')  # Redirect
        elif user_profile.is_writer:
                return redirect('writer_dashboard')  # Redirect
    else:
        # GET request, so pre-fill the form with the current profile picture
        pictureform = ProfilePictureForm(instance=user_profile)
        biographyform = ProfileBiographyForm(instance=user_profile)
    # Render the template with the form
    return render(request, 'update_profile_picture.html', {'pictureform': pictureform,'biographyform':biographyform, 'user_profile': user_profile})

def view_profile(request, id):
    
    user_profile = get_object_or_404(UserProfile, id=id)

    return render(request, 'view_profile.html', {'user_profile': user_profile})


def filter_feedbacks(request, id):
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None

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
            "feedback-template.html", {"feedbacks": feedbacks,'auth_user':user}, request=request
        )
        return JsonResponse({"status": "success", "feedback_html": feedback_html})

    return JsonResponse({"status": "error", "message": "Invalid request method"})

@csrf_exempt
def resolve_feedback(request, feedback_id):
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None

    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
        feedback.status = 'resolved'
        feedback.save()

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
            {'feedbacks': feedbacks,'auth_user':user},
            request=request
        )
        return JsonResponse({'status': 'success', 'feedback_html': feedback_html})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def delete_feedback(request, feedback_id):
    user = None
    try:
        user = UserProfile.objects.get(user_credentials=request.user)
    except UserProfile.DoesNotExist:
        user = None

    if request.method == 'POST':
        feedback = get_object_or_404(Feedback, id=feedback_id)
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
            {'feedbacks': feedbacks,'auth_user':user},
            request=request
        )
        return JsonResponse({'status': 'success', 'feedback_html': feedback_html})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def update_feedback(request, feedback_id):
    if request.method == "POST":
        feedback = get_object_or_404(Feedback, id=feedback_id)
        data = json.loads(request.body)
        feedback.comment = data.get("comment", feedback.comment)
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

        feedback = Feedback.objects.get(id=feedback_id)
        reply = Reply.objects.create(
            feedback=feedback,
            author=request.user.userprofile,  # Assuming the user is authenticated
            reply=reply_text
        )

        # Retrieve all replies for the feedback to update the UI
        replies = Reply.objects.filter(feedback=feedback)
        replies_html = render_to_string('replies-template.html', {'replies': replies},request=request)

        response_data = {
            'success': True,
            'replies_html': replies_html,
        }
        return JsonResponse(response_data)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
