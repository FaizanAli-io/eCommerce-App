from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('register', views.UserCreateView.as_view(), name='register'),
    path('login', views.TokenCreateView.as_view(), name='login'),
    path('logout', views.TokenDeleteView.as_view(), name='logout'),
    path('profile', views.UserDetailView.as_view(), name='profile'),
]
