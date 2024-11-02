from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Link the form to the Comment model
        fields = ['content']  # Specify the fields to include in the form
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'content-field',
                'placeholder': 'What do you think?',
                'rows': 3,  # You can specify the number of visible rows here
            }),
        }
