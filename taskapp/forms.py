from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name', 'password1', 'password2']

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # set 5 MB limit
                raise forms.ValidationError("Image file too large ( > 5MB )")
            if not picture.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Image must be in JPG or PNG format")
        return picture