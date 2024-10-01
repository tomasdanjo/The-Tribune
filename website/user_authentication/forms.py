from django import forms

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)), required=True) 
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    ROLES = [
        ('writer', 'Writer'),
        ('editor', 'Editor'),
    ]
    role = forms.ChoiceField(choices=ROLES, required=True)

class LogInForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)