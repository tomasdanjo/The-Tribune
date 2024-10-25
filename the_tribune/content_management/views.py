from django.shortcuts import render,get_object_or_404, redirect
from .forms import Article_Form, Photo_Form, Tag_Form
from user_authentication.models import UserProfile
from article.models import Tag, Article, Photo

# from django import form

# Create your views here.
def writer_dashboard_view(request):
    user = UserProfile.objects.get(user_credentials=request.user)

    articles = Article.objects.filter(writer = user)
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    submitted = articles.filter(status='submitted')
    archived = articles.filter(status='archived')

    context = {
        'user':user, 
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'submitted':submitted,
        'archived':archived

    }


    return render(request,'writer_dashboard.html',context)

def editor_dashboard_view(request):
    user = UserProfile.objects.get(user_credentials=request.user)

    articles = Article.objects.filter(writer = user)
    published = articles.filter(status='published')
    drafts = articles.filter(status='draft')
    submitted = articles.filter(status='submitted')
    archived = articles.filter(status='archived')
    to_approve = Article.objects.filter(editor=user)

    context = {
        'user':user, 
        'articles':articles,
        'published':published,
        'drafts':drafts,
        'archived':archived,
        'to_approve':to_approve

    }

    return render(request,'editor_dashboard.html',context)



def create_article(request):
    editors = UserProfile.objects.filter(is_editor=True)
    writer = UserProfile.objects.get(user_credentials=request.user)

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
    })

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    editors = UserProfile.objects.filter(is_editor=True)
    writer = article.writer  # Use the writer associated with the article

    if request.method == 'POST':
        article_form = Article_Form(request.POST, instance=article)
        photo_form = Photo_Form(request.POST, request.FILES, instance=article.photo)  # Include existing photo instance
        tag_form = Tag_Form(request.POST)

        if article_form.is_valid() and photo_form.is_valid() and tag_form.is_valid():
            # Save the Photo
            photo = photo_form.save()

            # Handle the Tag
            tag_name = tag_form.cleaned_data['tag_name']
            existing_tag = Tag.objects.filter(tag_name=tag_name).first()

            if existing_tag:
                tag = existing_tag
            else:
                tag = tag_form.save()  # Save new tag

            # Update the Article object
            article = article_form.save(commit=False)
            article.photo = photo
            article.tag = tag

            # Get the selected editor from the form
            editor_id = request.POST.get('editor')
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

            article.save()  # Save the updated article

            # Redirect based on user role
            if writer.is_writer:
                return redirect('writer_dashboard')
            elif writer.is_editor:
                return redirect('editor_dashboard')

    else:
        # Populate the forms with existing article data
        article_form = Article_Form(instance=article)
        photo_form = Photo_Form(instance=article.photo)
        tag_form = Tag_Form(initial={'tag_name': article.tag.tag_name})  # Prepopulate with existing tag name

    return render(request, 'edit_article_view.html', {
        'article_form': article_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'editors': editors,
        'writer': writer,
        'article':article,

    })


