from django.shortcuts import render,get_object_or_404, redirect
from article.models import Article
from .models import Comment, Subscription
from django.contrib import messages 
from django.utils import timezone
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
    comments = Comment.objects.filter(article_id=id)
    related_stories = Article.objects.filter(tag_id=article.tag_id).exclude(id=article.id)

    request.session['article_id'] = id
    print(id)

    return render(request,'full_article_view.html',{'article':article,'comments':comments,'related_stories':related_stories})

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