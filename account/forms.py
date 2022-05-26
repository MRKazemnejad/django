from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password',required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('this username already exists')
        return username

    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('Your email already exists')
        return email
    def clean(self):
        cd=super().clean()
        password=cd.get('password1')
        confirm=cd.get('password2')
        if password and confirm and password!=confirm:
            raise ValidationError('Your password should be the same')





class UserLoginForm(forms.Form):
    username=forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(required=True,widget=forms.PasswordInput(attrs={'class':'form-control'}))

class EditUserProfile(forms.ModelForm):
    email=forms.EmailField()
    class Meta:
        model=Profile
        fields=('age','title',)