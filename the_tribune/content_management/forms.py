# from django import forms
# from article.models import Article,Tag,Photo,Category

# class ArticleForm(forms.ModelForm):

#     class Meta:
#         model = Article
#         fields = ['tag','headline', 'category','status','photo', 'content']
        
#         widgets = {
#             'content': forms.Textarea(attrs={'rows': 5, 'cols': 40, 'placeholder': 'Write something meaningful',
#                                              'style':'align-self: stretch; flex: 1 1 0; padding-left: 100px; padding-right: 100px; padding-top: 40px; padding-bottom: 40px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25); border-radius: 15px; overflow: hidden; border: 1px rgba(70, 68, 92, 0.23) solid; justify-content: flex-start; align-items: flex-start; gap: 10px; display: inline-flex,flex: 1 1 0; align-self: stretch; color: black; font-size: 30px; font-family: Arimo; font-weight: 400; line-height: 40px; word-wrap: break-word'
#                                              }),
#             'headline': forms.TextInput(attrs={'placeholder': 'Enter article title',
#                                             'style':'align-self: stretch; padding-left: 2%; color: #596E9B; font-size: 50px; font-family: Oswald; font-weight: 500; text-transform: capitalize; word-wrap: break-word'
#                                             }),
#             'photo': forms.ClearableFileInput(attrs={'class': 'form-control','required': 'required'}),

#             'category': forms.Select(attrs={'class': 'form-control',
#                                              'style':'height: 47px; padding: 10px; color: #F2F2F2; font-size: 18px; font-family: Poppins; font-weight: 400; text-transform: uppercase; word-wrap: break-word;width: 200px; height: 47px; background: #596E9B; box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.25); border-radius: 15px;'
#                                              }),

#             'tag':forms.TextInput(attrs={'placeholder': 'Enter article tags',
#                                          'style':'align-self: stretch; padding-left: 2%; color: #46445C; font-size: 30px; font-family: Poppins; font-weight: 400; text-transform: uppercase; word-wrap: break-word'
#                                          }),
#         }

#     def save(self, commit=True):
#         article = super().save(commit)
    
#         tag_names = self.cleaned_data['tags'].split(',')
#         for tag_name in tag_names:
#             tag_name = tag_name.strip()  # Clean up whitespace
#             tag, created = Tag.objects.get_or_create(name=tag_name)  # Create or get the tag
#             article.tags.add(tag)  # Add the tag to the article
#         if commit:
#             article.save()
#         return article

from django import forms
from article.models import Article, Tag, Photo, Category

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['photo', 'caption', 'date_taken']
        widgets = {
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control', 
                'required': 'required',    
            }),
            'caption': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write something meaningful',
                'class': 'form-control'
            }),
            'date_taken': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',  # Use 'datetime-local' if you want time as well
            }),
        }

class CategoryForm(forms.ModelForm):
     class Meta:
        model = Category
        
        fields = ['category_name']
        widgets = {
        'category_name': forms.Select(attrs={
                'class': 'form-control', 
                'required': 'required',    
            }),
        }

class TagForm(forms.ModelForm):
     class Meta:
        model = Tag
        fields = ['tag_name']
        widgets = {
        'tag_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'required': 'required',    
            }),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['headline', 'content', 'status',] 
        
        widgets = {
            'headline': forms.TextInput(attrs={
                'placeholder': 'Enter article title',
                'class': 'form-control'
            }),

            'content': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': 'Write something meaningful',
                'class': 'form-control'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    # def save(self, commit=True):
    #     # Create the article instance
    #     article = super().save(commit=False)
        
    #     if commit:
    #         article.save()  # Save the article first
        
    #     # Handle tags if provided
    #     tag_names = self.cleaned_data.get('tag', '').split(',')
    #     for tag_name in tag_names:
    #         tag_name = tag_name.strip()
    #         if tag_name:  # Ensure tag name is not empty
    #             tag, created = Tag.objects.get_or_create(name=tag_name)
    #             article.tags.add(tag)  # Add the tag to the article

    #     return article


    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)  # Get the current user
    #     super().__init__(*args, **kwargs)
    #     if self.user:
    #         self.fields['writer'].initial = self.user  # Set the logged-in user as writer
    #         self.fields['editor'].initial = self.user  # Set the logged-in user as editor


    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Add any additional validation if needed
    #     return cleaned_data
