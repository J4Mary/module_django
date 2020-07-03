from django import forms
from django.forms import ModelForm

from . import models


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return self.data['password']

    def clean_username(self):
        if models.User.objects.filter(username__iexact=self.data.get('username').lower()):
            raise forms.ValidationError('Username already taken.')
        return self.data['username']


class UserInfo(ModelForm):
    class Meta:
        model = models.User
        fields = ['first_name', 'last_name', 'email', 'cash']
