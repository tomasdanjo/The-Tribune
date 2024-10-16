from django import forms
from article.models import Article, Category, Photo, Tag

class Article_Form(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'headline',
            'content',
            'editor',
            'photo',
            'tag',
            'category'
        ]
        widgets  = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter headline'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter article content'}),
            'editor': forms.Select(attrs={'class': 'form-select'}),
            'photo': forms.Select(attrs={'class': 'form-select'}),
            'tag': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

class Photo_Form(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            'photo',
            'caption',
            'date_taken'
        ]
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
            }),
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter a caption for the photo',
            }),
            'date_taken': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # This uses HTML5 date picker input
            }),
        }
