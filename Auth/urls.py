# urls.py
from django.urls import path
from Auth.views import register, user_login, view_profile, logout_view

app_name = "auth"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('view-profile/', view_profile, name='view_profile'),
    path('logout/', logout_view, name='logout'),
]
