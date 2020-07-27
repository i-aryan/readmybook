from django.contrib.auth.models import User
from django import forms
from .models import Profile, Book

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['username','email','password']

class LoginForm(forms.Form):
    username=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfilePostRegisterForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['firstName','lastName','bio','college']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['firstName','lastName','bio','college','image']

class NewBookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=['name','author','desc','image']
        labels={
            'image':'Book Cover Image',
            'name':'Book Title',
        }
        widgets = {
            'desc': forms.Textarea(attrs={'cols': 30, 'rows': 5}),
        }