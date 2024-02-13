from django.urls import path

from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('', views.CartViewSet)

app_name = 'sales'

urlpatterns = router.urls

urlpatterns += [
    path('transaction/<int:pk>', views.RetrieveTransactionsAPIView.as_view(),
         name='transaction')
]
