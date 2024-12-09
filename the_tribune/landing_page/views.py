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
from datetime import datetime
from article.models import Category
from user_authentication.models import UserProfile
from django.contrib.auth.models import AnonymousUser
# from transformers import pipeline

# summarizer = pipeline('summarization')  

def landing_page(request):
    article_id = request.session.get('article_id')
    
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user_credentials=request.user)
        except UserProfile.DoesNotExist:
            user = None  # Handle the case where no UserProfile is found
    else:
        user = None  # Handle unauthenticated users

    if article_id:  
        del request.session['article_id']  # Clear session after redirect
    
    current_date = datetime.now().strftime('%b %d, %Y')  

    articles = Article.objects.filter(status='published').order_by('-date_published')
    for article in articles:
        if timezone.is_naive(article.date_published):
            article.date_published = timezone.make_aware(article.date_published, timezone.get_current_timezone())
            article.save()
        
    top_stories = articles.annotate(
        num_likes=Count('comment__liked_by'),  # Count likes from comments
        num_comments=Count('comment'),  # Count number of comments
        tag_popularity=Count('tag__article')  # Count articles associated with the same tag
    )

    # Sort articles and limit to top 10
    top_stories = top_stories.order_by(
        '-num_likes',  # Highest likes  
        '-num_comments',  # Highest comments
        '-date_published',  # Most recent
        '-tag_popularity'  # Popular tag
    )[:9]

    news_articles = articles.filter(category__category_name="News")
    sports_articles=articles.filter(category__category_name="sports")
    entertainment_articles = articles.filter(category__category_name="entertainment")
    opinion_articles = articles.filter(category__category_name="opinion")
    technology_articles=articles.filter(category__category_name="technology")
    lifestyle_articles=articles.filter(category__category_name="lifestyle")
    editorial_articles=articles.filter(category__category_name="editorial")
    feature_articles=articles.filter(category__category_name="featured_topics")
    environment_articles=articles.filter(category__category_name="environment")
    scitech_articles=articles.filter(category__category_name="sci_and_tech")
    

    context =  {
        'articles': articles,
        'auth_user':user,
        'current_date':current_date,
        'news_articles':news_articles,
        'sports_articles':sports_articles,
        'entertainment_articles':entertainment_articles,
        'opinion_articles':opinion_articles,
        'technology_articles':technology_articles,
        'lifestyle_articles':lifestyle_articles,
        'editorial_articles':editorial_articles,
        'feature_articles':feature_articles,
        'environment_articles':environment_articles,
        'scitech_articles':scitech_articles,
        'top_stories':top_stories,
        'show_search':True
    
    }

            
    return render(request, 'landing_page.html',context)

def full_article(request, id):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user_credentials=request.user)
        except UserProfile.DoesNotExist:
            user = None  # Handle the case where no UserProfile is found
    else:
        user = None 

    article = get_object_or_404(Article,id=id)
    comment_count = Comment.objects.filter(article_id=id).count()
    comments = Comment.objects.filter(article_id=id).order_by('-date_published')[:5]
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id).order_by('-date_published')[:3]
    related_stories_count = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id).order_by('-date_published').count()

    request.session['article_id'] = id
    print("Comment count: ",comment_count)

    comment_form = CommentForm()
    current_date = datetime.now().strftime('%b %d, %Y') 
    context = {
        'article':article,
        'comments':comments,
        'comment_count':comment_count,
        'related_stories':related_stories,
        'comment_form':comment_form,
        'related_stories_count':related_stories_count,
        'auth_user':user,
        'current_date':current_date,
        'show_search':True
    }

    return render(request,'full_article_view.html',context)

def load_more_comments(request, article_id, offset):

    sort_by = request.session.get('sort_by')
    sort = ""
    offset = int(offset)
    comments_query = Comment.objects.filter(article_id=article_id)
    if sort_by == 'oldest':
        sort = 'date_published'
    elif sort_by == 'relevant':
        sort = '-like_count'
    else:  # Default to newest
        sort = '-date_published'

    offset = int(offset)
    comments = Comment.objects.filter(article_id=article_id).order_by(sort)[offset:offset + 5]
    total_comments = comments_query.count()
    comments_html = render_to_string('comments.html', {'comments': comments}, request=request)
    more_comments_available = offset + 5 < total_comments

    return JsonResponse({
        'comments_html': comments_html,
        'comment_count': len(comments), 
        'more_comments_available': more_comments_available,
    })




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

def summarize_article(request,article_id):
    pass
    article=Article.objects.get(id=article_id)
    text = f"{article.headline}\n\n{article.content}"

    try:
        summary = summarizer(
            text, max_length=300, min_length=150, do_sample=False
        )[0]['summary_text']
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'summary': summary})


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

def view_profile(request, id):
    user_profile = get_object_or_404(UserProfile, id=id)
    
    return render(request, 'view_profile.html', {'user_profile': user_profile,})

def about_us(request):
    current_date = datetime.now().strftime('%b %d, %Y')  
    context = {
        'show_search':True,
        'current_date':current_date

    }
    return render(request, 'about-us.html',context)

def mission_statement(request):
    current_date = datetime.now().strftime('%b %d, %Y')  
    context = {
        'show_search':True,
        'current_date':current_date

    }
    return render(request, 'mission-statement.html',context)

def ai_guidelines(request):
    return render(request, 'ai-guidelines.html')

def the_team(request):
    return render(request, 'the-team.html')

def job_openings(request):
    return render(request, 'job-opening.html')

def contact_us(request):
    return render(request, 'contact-us.html')