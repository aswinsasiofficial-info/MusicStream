from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(forms.ModelForm):
    """Form for creating new users"""
    email = forms.EmailField(required=True)
    username = forms.CharField(required=False)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User
        fields = ('email', 'username')
        
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


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
