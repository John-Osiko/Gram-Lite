from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Image, Comment

class SignUpForm(forms.ModelForm):
    email = forms.EmailField(label = 'Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Invalid email address/Email address required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'location', 'profile_picture', 'bio']


class PostForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'caption')


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['comment'].widget = forms.TextInput()
        self.fields['comment'].widget.attrs['placeholder'] = 'Add a comment...'

    class Meta:
        model = Comment
        fields = ('comment',)