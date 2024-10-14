from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import Login_Form, Signup_Form
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.

def login_view(request):
    if request.method == "POST":
        form = Login_Form(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                user_profile = UserProfile.objects.get(user=user)
                if user_profile.is_writer:
                    return redirect('writer-dashboard')
                elif user_profile.is_editor:
                    return redirect('editor-dashboard')
            else:
                messages.error(request,'Invalid email or password')

    else:
        form = Login_Form()
    
    return render(request,'user_authentication/login.html',{'form':form})
    
def signup_view(request):
    if request.method =="POST":
        form = Signup_Form(request.POST)
        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']

                # Check if the email already exists
                if UserProfile.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already registered. Please log in.')
                    return redirect('signup')  # Adjust as necessary

                # Create the user and save it
                user = User.objects.create_user(username=email, email=email, password=password)
                user_profile = UserProfile.objects.create(user=user, email=email)  # Create the user profile
                messages.success(request, 'Your account has been created successfully! You can now log in.')
                return redirect('login')  # Adjust as necessary
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}") 
    else:
        form = Signup_Form()
    
    return render(request,'user_authentication/signup.html',{'form':form})

