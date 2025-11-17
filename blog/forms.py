from django.forms import ModelForm, TextInput, EmailInput, Textarea
from .models import Article, Profile, Comment, Click
from django.contrib.auth.models import User

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', ]

        labels = {
            'username': '',
            'email': '',
            'password': '',
            'first_name': '',
            'last_name': '',
        }

        widgets = {
            'username': TextInput(attrs={'class': 'form-control', 'placeholder': 'User Name'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': TextInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),

        }

        error_messages = {
            'user_name': {}
        }

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile', 'country', 'state', 'mobile',]

        widgets = {
            # 'user_type': TextInput(attrs={'class': 'form-control', 'placeholder': 'user_type'}),
            'country': TextInput(attrs={'class': 'form-control', 'placeholder': 'country'}),
            'state': TextInput(attrs={'class': 'form-control', 'placeholder': 'state'}),
            'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': 'mobile'}),
        }

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'cover', 'content', 'summary', 'category', ]

        labels = {
            'title': 'Add Title',
            'cover': 'Select a cover image',
            'content': '',
            'summary': '',
            'category': 'select category',
        }

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            # 'cover': EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'content': Textarea(attrs={'class': 'form-control', "id": "summernote", 'placeholder': 'Text'}),
            'summary': Textarea(attrs={'class': 'form-control', "cols": 100, "rows": 3, 'placeholder': 'Summary'}),
            # 'category': TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
        }

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment',]
#         labels = {'comment': 'What do you think?',}
#         widgets = {
#             'comment': TextInput(attrs={'class': 'form-control', 'placeholder': 'Comment'}),
#         }