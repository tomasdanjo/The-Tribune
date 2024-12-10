from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import Login_Form, Signup_Form
from django.contrib.auth.models import User
from .models import UserProfile
from landing_page.views import full_article

# Create your views here.


def login_view(request):
    from_sidebar = request.GET.get('from_sidebar')
    if from_sidebar:
        request.session['from_sidebar'] = True

    article_id = request.GET.get('article_id')
    if article_id:
        request.session['article_id'] = article_id

    if request.method == "POST":
        form = Login_Form(request.POST)
        if form.is_valid():
            try:
                username_or_email = form.cleaned_data['username']
                password = form.cleaned_data['password']

                # Check if the input is an email
                if '@' in username_or_email and User.objects.filter(email=username_or_email).exists():
                    # Get the associated username for email login
                    username = User.objects.get(email=username_or_email).username
                else:
                    # Use the input as the username
                    username = username_or_email
                
                user = authenticate(request, username=username, password=password)

                if user is not None:
                    login(request, user)
                    if request.user.is_authenticated:  # Check if login was successful

                        user_profile = UserProfile.objects.get(user_credentials = user)
                        if user_profile.user_credentials == user:
                            if user_profile.is_writer:
                                #messages.success(request, 'Login successful! but  writer')
                                return redirect('writer_dashboard')
                                #return to reader writer
                            elif user_profile.is_editor:
                                #return to reader editor
                                #messages.success(request, 'Login successful! but  editor')
                                return redirect('editor_dashboard')  
                            elif user_profile.is_reader:
                                article_id = request.session.get('article_id')
                                from_sidebar = request.session.get('from_sidebar')
                                if article_id:
                                    print(article_id)
                                    del request.session['article_id']  # Clear session after redirect
                                    return redirect('full_article_view', id=article_id)
                                elif from_sidebar:
                                    del request.session['from_sidebar']
                                    return redirect('home')
                                else:
                                    messages.info(request, 'Login successful! Redirecting to home.')
                                    return redirect('home')
                                 
                    else:
                        messages.error(request, 'Login failed, please try again.')
                else:
                    messages.error(request, 'Invalid username or password.')
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = Login_Form()
    
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == "POST":
        form = Signup_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please log in.')
                return redirect('signup')

            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email,
                    password=form.cleaned_data['password'],
                )

                # Create the user profile

                article_id = request.session.get('article_id')
                from_sidebar = request.session.get('from_sidebar')

                if article_id or from_sidebar:
                    is_reader = True
                else:
                    is_reader = False

                UserProfile.objects.create(
                    user_credentials=user,  # Use user_credentials instead of user

                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=email,

                    is_writer = not is_reader,
                    is_editor = False,
                    is_reader = is_reader
                )
                messages.success(request, 'Your account has been created successfully! You can now log in.')
                return redirect('login')

            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}") 
    else:
        form = Signup_Form()

    return render(request, 'signup.html', {'form': form})

def signup_user_view(request):
    if request.method == "POST":
        form = Signup_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already registered. Please log in.')
                return redirect('signup')

            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=email,
                    password=form.cleaned_data['password'],
                )

                # Create the user profile
                UserProfile.objects.create(
                    user_credentials=user,  # Use user_credentials instead of user

                    first_name=user.first_name,
                    last_name=user.last_name,
                    email=email,

                    is_writer = False,
                    is_editor = False,
                    is_reader = True
                )
                messages.success(request, 'Your account has been created successfully! You can now log in.')
                article_id = request.session['article_id']
                print(article_id)
                messages.success(request, 'Login successful! Redirecting to article.')
                return redirect('full_article_view',article_id)

            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}") 
    else:
        form = Signup_Form()

    return render(request, 'signup.html', {'form': form})

