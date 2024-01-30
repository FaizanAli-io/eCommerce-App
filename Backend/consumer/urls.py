from rest_framework.routers import SimpleRouter

from .views import ConsumerViewSet

router = SimpleRouter()
router.register('', ConsumerViewSet)

app_name = 'user'
urlpatterns = router.urls
