from django.shortcuts import render, redirect
from .forms import SignUpForm, LogInForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import UserProfile
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    username=form.cleaned_data['username'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],  
                )

                UserProfile.objects.create(
                    user_credentials=user,  # Link the profile to the user
                    birthdate=form.cleaned_data['birthdate'],  
                    role='writer',
                )
                messages.success(request, "Registration successful! You can now log in.")
                return redirect('login')
            except Exception as e:
                # Handle specific exceptions if needed
                #form.add_error(None, f"An error occurred: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}") 
    else:
        
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
            
                user = authenticate(request, username=username, password=password)
            
                if user is not None:
                    userprofile = UserProfile.objects.get(user_credentials=user)
                    auth_login(request, user) 
                    messages.success(request, f"User: {user.username} with role: {userprofile.role} Login successful!")
                else:
                    messages.error(request, "Failed to log in. Please check your email and password.") 
            except Exception as e:
                form.add_error(None, f"An error occurred: {str(e)}")
    else:
        form = LogInForm()
    
    return render(request,'login.html',{'form':form})
            
            
