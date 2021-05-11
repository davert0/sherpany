from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Event, Profile
from django.forms import ModelForm
from .widgets import BootstrapDateTimePickerInput

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email', 'password1', 'password2')


class UserUpdateForm(ModelForm):
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('email',)


class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)


class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'event_date': BootstrapDateTimePickerInput(format='%m/%d/%Y %H:%M'),
        }
# 'event_date': forms.SelectDateWidget(attrs={'class': 'form-control', }),

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
