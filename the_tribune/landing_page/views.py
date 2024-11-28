from django.shortcuts import render,get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from article.models import Article
from .models import Comment, Subscription
from django.contrib import messages 
from django.utils import timezone
from .forms import CommentForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.templatetags.static import static
from django.db.models import Count
# from myapp.models import Article

def landing_page(request):
    article_id = request.session.get('article_id')
    if article_id:
        del request.session['article_id']  # Clear session after redirect

    articles = Article.objects.filter(status    ='published')
    for article in articles:
        if timezone.is_naive(article.date_published):
            article.date_published = timezone.make_aware(article.date_published, timezone.get_current_timezone())
            article.save()
            
    return render(request, 'landing_page.html', {'articles': articles})

def full_article(request, id):
    article = get_object_or_404(Article,id=id)
    comment_count = Comment.objects.filter(article_id=id).count()
    comments = Comment.objects.filter(article_id=id).order_by('-date_published')[:5]
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id)[:3]
    related_count = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id).count()

    request.session['article_id'] = id
    print(id)

    comment_form = CommentForm()

    return render(request,'full_article_view.html',{'article':article,
                                                    'comments':comments,
                                                    'comment_count':comment_count,
                                                    'related_stories':related_stories,
                                                    'related_count':related_count,
                                                    'comment_form':comment_form})

def load_more_comments(request, article_id, offset):
    
    sort_by = request.session.get('sort_by')
    sort=""

    if sort_by == 'oldest':
        sort='date_published'
    elif sort_by == 'relevant':
        sort='-like_count'
    else:  # Default to newest
        sort='-date_published'
    
    comments = Comment.objects.filter(article_id=article_id).order_by(sort)[offset:offset + 5]

    comments_html=render_to_string('comments.html', {'comments': comments}, request=request)
   
    
    return JsonResponse({
        'comments_html': comments_html, 
        'comment_count': len(comments)  # Pass the count of comments retrieved
    })




def load_more_related_stories(request, article_id, offset):
    # Get the current article to fetch its tag_id
    article = get_object_or_404(Article, id=article_id)
    
    # Get the related stories based on the tag of the current article, excluding the current article
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id)[offset:offset + 3]
    
    # Prepare the data to send back as JSON
    related_stories_data = [
        {
            'headline': story.headline,
            'url': story.get_absolute_url(),
            'writer_name': f"{story.writer.first_name} {story.writer.last_name}",
            'date_published': story.date_published.strftime('%B %d, %Y'),
            'photo_url': story.photo.url if story.photo else None
        }
        for story in related_stories
    ]
    
    return JsonResponse({'related_stories': related_stories_data})


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Check if the email naa ni exist na ang email
            if Subscription.objects.filter(email=email).exists():
                messages.info(request, 'You are already subscribed with this email.')
            else:
                # Create new
                Subscription.objects.create(email=email)
                messages.success(request, 'Successfully subscribed to the newsletter!')
            return redirect('home')
        else:
            messages.error(request, 'Please provide a valid email address.')
            return redirect('home')
    else:
        # Optionally, handle GET requests or redirect
        return redirect('home')
    


# @require_POST
# @login_required
# def add_comment(request, article_id):
#     article_instance = get_object_or_404(Article, id=article_id)
#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
        
#         if comment_form.is_valid():
#             Comment.objects.create(
#                 article=article_instance,  # Set the article instance
#                 commenter=request.user.userprofile,  # Set the commenter
#                 content=comment_form.cleaned_data['content']  # Use the cleaned data from the form
#             )

#             # Redirect back to the full article view with updated comments
#             return redirect('full_article_view', id=article_id)
        
#     return redirect('full_article_view', id=article_id)

@require_POST
def add_comment(request, article_id):
    content = request.POST.get('content', '').strip()
    article = get_object_or_404(Article, id=article_id)
    
    
    if content:  # Make sure the content is not empty
        comment = Comment.objects.create(
            article=article,
            commenter=request.user.userprofile,
            content=content
        )
        
        # Fetch updated comments
        comments = Comment.objects.filter(article=article).order_by('-date_published')

        
        # Render the updated comments to a partial template
        comments_html = render(request, 'comments.html', {'comments': comments}).content.decode('utf-8')

        return JsonResponse({'comments_html': comments_html,'comment_count':comments.count()})
    else:
        return JsonResponse({'error': 'Comment cannot be empty.'}, status=400)


@login_required
@require_POST
def like_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.get(id=comment_id)
    user_profile = request.user.userprofile

    # Initialize user_liked and user_disliked
    user_liked = False
    user_disliked = False

    if user_profile in comment.liked_by.all():
        # If already liked, remove like
        comment.liked_by.remove(user_profile)
        user_liked = False
    else:
        # Add like
        comment.liked_by.add(user_profile)
        user_liked = True

        # Remove dislike if exists
        if user_profile in comment.disliked_by.all():
            comment.disliked_by.remove(user_profile)
        user_disliked = False

    context = {
        'likes': comment.liked_by.count(),
        'dislikes': comment.disliked_by.count(),
        'user_disliked': user_disliked,
        'user_liked': user_liked
    }

    return JsonResponse(context)


@login_required
@require_POST
def dislike_comment(request):
    comment_id = request.POST.get('comment_id')
    comment = Comment.objects.get(id=comment_id)
    user_profile = request.user.userprofile

    # Initialize user_liked and user_disliked
    user_liked = False
    user_disliked = False

    if user_profile in comment.disliked_by.all():
        # If already disliked, remove dislike
        comment.disliked_by.remove(user_profile)
        user_disliked = False
    else:
        # Add dislike
        comment.disliked_by.add(user_profile)
        user_disliked = True

        # Remove like if exists
        if user_profile in comment.liked_by.all():
            comment.liked_by.remove(user_profile)
        user_liked = False

    context = {
        'likes': comment.liked_by.count(),
        'dislikes': comment.disliked_by.count(),
        'user_disliked': user_disliked,
        'user_liked': user_liked
    }

    return JsonResponse(context)


def sort_comments(request, article_id):
    sort_by = request.GET.get('sort_by', 'newest')
    request.session['sort_by']=sort_by
    print(f"Sort by: {sort_by}")
    comments = Comment.objects.filter(article_id=article_id)

    # Sort comments based on the chosen method
    if sort_by == 'oldest':
        comments = comments.order_by('date_published')[:5]
    elif sort_by == 'relevant':
        comments = comments.annotate(like_count=Count('liked_by')).order_by('-like_count')[:5]
    else:  # Default to newest
        comments = comments.order_by('-date_published')[:5]

    # Render the comments to a partial template
    comments_html = render(request, 'comments.html', {'comments': comments}).content.decode('utf-8')

    return JsonResponse({'comments_html': comments_html})


def delete_comment(request, comment_id):
    # Ensure the request method is DELETE
    if request.method == 'DELETE':
        # Fetch the comment object
        comment = get_object_or_404(Comment, id=comment_id)

        # Check if the user is the commenter
        if comment.commenter == request.user.userprofile:
            # Delete the comment
            comment.delete()

            # Fetch updated comments
            comments = Comment.objects.filter(article=comment.article).order_by('-date_published')

            # Render the updated comments to a partial template
            comments_html = render(request, 'comments.html', {'comments': comments}).content.decode('utf-8')

            return JsonResponse({'comments_html': comments_html, 'comment_count': comments.count()})
        else:
            return JsonResponse({'error': 'You are not authorized to delete this comment.'}, status=403)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
