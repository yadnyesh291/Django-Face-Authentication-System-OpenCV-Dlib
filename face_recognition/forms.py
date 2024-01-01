from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','username', 'email', 'password' ]

    # Add any additional form field customization or validation here if needed
