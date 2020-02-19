from blog.models import models, Account
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Community


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            'username',
            'password'
        )


class RegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')


class EditProfileForm(UserChangeForm):
    class Meta:
        model = Account
        fields = (
            'first_name',
            'last_name',
            'date_of_birth',
            'avatar',
            'email'
        )


class EditCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = (
            'name',
            'description',
            'creator',
            'img_community',
        )


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = (
            'name',
            'description',
        )