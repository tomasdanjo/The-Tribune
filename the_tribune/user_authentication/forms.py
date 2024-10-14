from django import forms 
from django.contrib.auth.models import User

class Login_Form(forms.Form):
    email = forms.EmailField(label='Email',max_length=254,required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'Password',
            'style': 'flex: 1 1 0; width: 500px; height: 45px;padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'enter your password'
        }),
        required=True
    )
class Signup_Form(forms.Form):
    first_name = forms.CharField(       
        widget=forms.TextInput(attrs={
            'class': 'FirstName',
            'style': 'flex: 1 1 0; width: 300px; height: 45px; padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'first name'
        }),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'LastName',
            'style': 'flex: 1 1 0; width: 200px; height: 45px;padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'last name'
        }),
        required=True
    )
    username = forms.CharField(       
        widget=forms.TextInput(attrs={
            'class': 'Username',
            'style': 'flex: 1 1 0; width: 500px; height: 45px; padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'username'
        }),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'Email',
            'style': 'flex: 1 1 0; width: 500px; height: 45px;padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'email'
        }),
        required=True,
    )


    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'Password',
            'style': 'flex: 1 1 0; width: 500px; height: 45px;padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'password'
        }),
        required=True
    )

    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'ConfirmPassword',
            'style': 'flex: 1 1 0; width: 500px; height: 45px;padding-left: 20px; padding-right: 20px; justify-content: flex-start; align-items: center; background: #F2F2F2; border-radius: 15px; border: 1px #596E9B solid; display: flex',
            'placeholder': 'confirm password'
        }),
        required=True
    )
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
             self.add_error("email","This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data
    



