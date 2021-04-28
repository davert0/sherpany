from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('', index, name='home'),
    path('add_event/', add_event, name='add_event'),
    path('logout/', user_logout, name='logout'),
    path('event/<int:event_id>/', view_event, name='view_event'),
]