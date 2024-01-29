from rest_framework.routers import SimpleRouter

from .views import ConsumerViewSet

router = SimpleRouter()
router.register('', ConsumerViewSet)

urlpatterns = router.urls
