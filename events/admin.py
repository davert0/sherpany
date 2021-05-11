from django.contrib import admin
from .models import Event, CustomUser, Profile
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username', ]



admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Event)
admin.site.register(Profile)
