from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

VERSION = 2.0

urlpatterns = [
    path(f'v{VERSION}/admin/', admin.site.urls),
    path(f'v{VERSION}/user/', include('user.urls')),
    path(f'v{VERSION}/sales/', include('sales.urls')),
    path(f'v{VERSION}/product/', include('product.urls')),

    path(f'v{VERSION}/api/schema/',
         SpectacularAPIView.as_view(), name='api-schema'),
    path(f'v{VERSION}/api/docs/', SpectacularSwaggerView.as_view(
        url_name='api-schema'), name='api-docs'),
]
