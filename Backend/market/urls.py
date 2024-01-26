from rest_framework.routers import SimpleRouter

from .views import (
    VendorViewSet,
    ProductViewSet,
)

router = SimpleRouter()
router.register('vendors', VendorViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
