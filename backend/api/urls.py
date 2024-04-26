from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from api.views import CollectViewSet, PaymentViewSet

router = DefaultRouter()
router.register('collects', CollectViewSet, basename='collects')
router.register(
    r'collects/(?P<collect_id>\d+)/payments',
    PaymentViewSet,
    basename='payments',
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
        ),
        name='swagger-ui',
    ),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]
