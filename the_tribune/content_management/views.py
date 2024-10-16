from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from article.models import Article,Tag,Photo,Category
from user_authentication.models import UserProfile  
from .forms import ArticleForm,PhotoForm,TagForm,CategoryForm

@login_required
def writer_dashboard_view(request):
    # Get the UserProfile for the logged-in user
    user_profile = UserProfile.objects.get(user_credentials=request.user)

    # Filter articles by the currently logged-in user's writer profile
    articles = Article.objects.filter(writer=user_profile,status__in=['published'])

    return render(request, 'writer_dashboard.html', {'articles': articles})

@login_required
def writer_dashboard_view_rejected(request):
    # Get the UserProfile for the logged-in user
    user_profile = UserProfile.objects.get(user_credentials=request.user)

    status_filter = request.GET.get('status', 'rejected')
    # Filter articles by the currently logged-in user's writer profile
    articles = Article.objects.filter(writer=user_profile).filter(status = status_filter)

    return render(request, 'writer_dashboard.html', {'articles': articles})

@login_required
def writer_dashboard_view_pending(request):
    # Get the UserProfile for the logged-in user
    user_profile = UserProfile.objects.get(user_credentials=request.user)
    # Filter articles by the currently logged-in user's writer profile
    articles = Article.objects.filter(writer=user_profile,status__in=['in_review','revision','submitted'])

    return render(request, 'writer_dashboard.html', {'articles': articles})

@login_required
def writer_create_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)
        category_form = CategoryForm(request.POST)

        if (article_form.is_valid() and 
            photo_form.is_valid() and 
            tag_form.is_valid() and 
            category_form.is_valid()):
            try:
                user_profile = UserProfile.objects.get(user_credentials=request.user)

                # Save the photo instance
                photo = Photo.objects.create(
                    photo=photo_form.cleaned_data['photo'],
                    caption=photo_form.cleaned_data['caption'],
                    date_taken=photo_form.cleaned_data['date_taken'],
                )
                photo.save()
                # Save the tag instance
                tag = Tag.objects.create(
                    tag_name=tag_form.cleaned_data['tag_name'],
                )
                tag.save()
                # Save the category instance
                category = Category.objects.create(
                    category_name=category_form.cleaned_data['category_name']
                )
                category.save()
                # Create and save the article instance
                article = Article.objects.create(
                    headline=article_form.cleaned_data['headline'],
                    content=article_form.cleaned_data['content'],
                    status=article_form.cleaned_data['status'],

                    writer=user_profile,
                    editor=user_profile,
                    
                    photo=photo,
                    tag=tag,
                    category=category,
                )
                article.save()
                return redirect('writer_dashboard') 

            except Exception as e:
                # Add an error to the article form
                article_form.add_error(None, f"An error occurred: {str(e)}") 
    else:
        article_form = ArticleForm()
        photo_form = PhotoForm()
        tag_form = TagForm()
        category_form = CategoryForm()

    return render(request, 'writer_create_article.html', {
        'article_form': article_form,
        'photo_form': photo_form,
        'tag_form': tag_form,
        'category_form': category_form,
    })

# def editor_dashboard_view(request):
#     pass