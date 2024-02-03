from rest_framework.routers import SimpleRouter

from .views import ProductViewSet

router = SimpleRouter()
router.register('', ProductViewSet)

app_name = 'product'
urlpatterns = router.urls
