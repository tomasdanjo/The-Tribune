from django import forms
from article.models import Article, Category, Photo, Tag

class Article_Form(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'headline',
            'content',
            'editor',
            'category'
        ]
        widgets = {
            'headline': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter headline'
            }),
            'content': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter article content',
                'rows': 10  # Optional: adjust the number of rows for the textarea
            }),
            'editor': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            }),
            'category': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
            }),
        }

class Tag_Form(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            'tag_name'
        ]
        widgets = {
            'tag_name': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter Tag'
            }),
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
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'accept': 'image/*'
            }),
            'caption': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'placeholder': 'Enter a caption for the photo'
            }),
            'date_taken': forms.DateInput(attrs={
                'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline',
                'type': 'date'  # HTML5 date picker
            }),
        }
