import datetime
import re
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
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

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['company_name', 'location', 'birthdate', 'phone']
        
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            phone = str(phone).strip()
        if phone and not phone.isdigit():
            raise forms.ValidationError("Phone number should contain only digits.")
        return phone
    
    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate and birthdate > datetime.date.today():
            raise forms.ValidationError("Birthdate cannot be in the future.")
        return birthdate
    
    def clean_company_name(self):
        company_name = self.cleaned_data.get('company_name')
        if not company_name:
            raise forms.ValidationError("Company name cannot be empty.")
        return company_name
    
    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise forms.ValidationError("Location cannot be empty.")
        return location

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    
class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current password'}),
    )
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new password'}),
    )
    new_password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
    )

    def clean_new_password1(self):
        new_password1 = self.cleaned_data.get('new_password1')
        if len(new_password1) < 8:
            raise forms.ValidationError("The new password must be at least 8 characters long.")
        if not re.findall(r'\d', new_password1):
            raise forms.ValidationError("The new password must contain at least one digit.")
        if not re.findall(r'[A-Za-z]', new_password1):
            raise forms.ValidationError("The new password must contain at least one letter.")
        return new_password1

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The two password fields must match.")
        return new_password2