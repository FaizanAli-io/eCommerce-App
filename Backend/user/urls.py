from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserListView.as_view(), name='list'),
    path('token', views.CreateTokenView.as_view(), name='token'),
    path('profile', views.UserDetailView.as_view(), name='profile'),
]
