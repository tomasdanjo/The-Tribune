from django.shortcuts import render
from article.models import Article, Category, Tag
from datetime import datetime
from user_authentication.models import UserProfile

from django.db.models import Q
from django.shortcuts import render
from datetime import date
import calendar

def search_article(request):
    

    current_year = datetime.now().year
    years = range(2000, current_year + 1)[::-1]
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    query = request.GET.get('query', '')
    start_year = request.GET.get('start_year')
    start_month = request.GET.get('start_month')
    end_year = request.GET.get('end_year')
    end_month = request.GET.get('end_month')
    has_tag = request.GET.get('has_tag')
    category_id = request.GET.get('category')
    place = request.GET.get('place')

    articles = Article.objects.all()

    # Search by headline or content
    if query:
        articles = articles.filter(
            Q(headline__icontains=query) | 
            Q(content__icontains=query)
        )

    # Handle date filtering with valid dates
    start_date = None
    end_date = None

    orig_start_month = start_month
    orig_end_month = end_month

    if start_month in months:
        start_month = months.index(start_month)+1
    if end_month in months:
        end_month = months.index(end_month)+1

    if start_year:
        start_month = start_month or 1  # Default to January if no start_month is provided
        start_date = date(int(start_year), int(start_month), 1)

    if end_year:
        end_month = end_month or 12  # Default to December if no end_month is provided
        # Get the last day of the selected end_month
        last_day = calendar.monthrange(int(end_year), int(end_month))[1]
        end_date = date(int(end_year), int(end_month), last_day)

    # Filter by the date range if both start and end dates are provided
    if start_date and end_date:
        articles = articles.filter(date_published__range=[start_date, end_date])
    elif start_date:
        articles = articles.filter(date_published__gte=start_date)
    elif end_date:
        articles = articles.filter(date_published__lte=end_date)

    # Filter by tags if 'has_tag' is selected
    if has_tag:
        articles = articles.filter(tag_id__isnull=False)

    # Filter by category
    if category_id:
        articles = articles.filter(category_id=category_id)

    # Filter by place
    if place:
        articles = articles.filter(place__icontains=place)

    # Fetch all tags and categories for filters
    tags = Tag.objects.all()
    categories = Category.objects.all()

    current_date = datetime.now().strftime('%b %d, %Y')  
   
    context = {
        'articles': articles,
        'tags': tags,
        'categories': categories,
        'years': years,
        'months': months,
        'query': query,
        'start_year': start_year,
        'start_month': orig_start_month,
        'end_year': end_year,
        'end_month': orig_end_month,
        'has_tag': has_tag,
        'category_id': category_id,
        'current_date':current_date,
        
    }

    return render(request, 'search_results.html', context )
