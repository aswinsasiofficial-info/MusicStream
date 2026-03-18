from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users"""
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    """Form for updating user information"""
    
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('email', 'username', 'avatar', 'bio')


class ProfileUpdateForm(forms.ModelForm):
    """Simplified profile update form"""
    
    class Meta:
        model = User
        fields = ['username', 'avatar', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
        }
