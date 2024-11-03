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
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve the writer (UserProfile) passed to the form
        super(Article_Form, self).__init__(*args, **kwargs)

        # If the user is not passed or is not a writer, make the editor field optional
        if self.user is None or not getattr(self.user, 'is_writer', False):
            self.fields['editor'].required = False

    def clean(self):
        cleaned_data = super().clean()

        # Check if user is passed and if they are a writer, validate the editor field
        if self.user and getattr(self.user, 'is_writer', False):
            editor = cleaned_data.get("editor")
            if not editor:
                self.add_error('editor', "An editor must be selected.")
                
        return cleaned_data

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

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        
        # If there's an existing photo, don't require a new one
        if not photo and self.instance.pk:  # Check if the instance exists (is being edited)
            return self.instance.photo  # Return the existing photo
        
        return photo  # Return the new photo if uploaded
