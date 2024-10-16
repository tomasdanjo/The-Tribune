from django.shortcuts import render, redirect
from .forms import Article_Form, Photo_Form
from user_authentication.models import UserProfile

# Create your views here.
def writer_dashboard_view(request):
    user = request.user

    return render(request,'writer_dashboard.html',{'user':user})

def create_article(request):
    if request.method == 'POST':
        article_form  = Article_Form(request.POST)
        photo_form = Photo_Form(request.POST, request.FILES)

        if article_form.is_valid() and photo_form.is_valid():
            photo = photo_form.save()

            article = form.save(commit=False)
            headline = form.cleaned_data['headline']
            content = form.cleaned_data['content']
            editor = form.cleaned_data['editor']
            photo = form.cleaned_data['photo']
            tag = form.cleaned_data['tag']
            category = form.cleaned_data['category']

            article.writer = UserProfile.objects.get(user_credentials=request.user)
            article.headline = headline
            article.content =content
            article.editor =editor
            article.photo = photo
            article.tag = tag
            article.category = category
            

            action = request.POST.get('action')
            if action=="save_draft":
                article.status = "draft"
            elif action == "submit":
                article.status = "submitted"

            article.save()

            if article.writer.is_writer:
                return redirect('writer_dashboard')
            elif article.writer.is_editor:
                return redirect('editor_dashboard')
    else:
        article_form = Article_Form()
        photo_form = Photo_Form()
        editors = UserProfile.objects.filter(is_editor=True)


    return render(request,'create_article.html',{'article_form':article_form,'photo_form':photo_form,'editors':editors})

