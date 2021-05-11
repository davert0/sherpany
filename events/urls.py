from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # path('register/', register, name='register'),
    # path('login/', user_login, name='login'),
    path('add_event/', add_event, name='add_event'),
    # path('logout/', user_logout, name='logout'),
    path('event/<int:event_id>/', view_event, name='view_event'),
    path('event/<int:event_id>/update', edit_event, name='edit_event'),
    path('profile/<str:username>', Profile.as_view(), name='profile'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('my_events/', MyEventsView.as_view(), name='my_events')
]
