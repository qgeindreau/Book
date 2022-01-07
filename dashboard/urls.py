from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    dashboard,
    profile,
    profile_edit,
    messages,
    messages_api,
    projets,
    projets_api,
    LoginView,    )

app_name = 'dashboard'
urlpatterns = [

    path('', dashboard, name='dashboard'),

    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),

    path('messages', messages, name='messages'),
    path('messages/api/', messages_api, name='messages_api'),

    path('projets', projets, name='projets'),
    path('projets/api/', projets_api, name='projets_api'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
