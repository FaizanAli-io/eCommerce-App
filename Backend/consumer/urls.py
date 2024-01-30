from django.urls import path

from . import views

app_name = 'consumer'

urlpatterns = [
    path('', views.ConsumerListView.as_view(), name='list'),
    path('token', views.CreateTokenView.as_view(), name='token'),
    path('<int:pk>', views.ConsumerDetailView.as_view(), name='detail'),
]
