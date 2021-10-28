from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from order.views_api import OrderItemAPI, OrderAPIView
from product.views_api import ProductAPIView, FeatureAPIView
from profile.views_api import ImportProductsView, ConfirmationSent

API_VERSION = [None, 'v1/']
API_BASE_URL = 'api'

router = routers.DefaultRouter()
router.register('product', ProductAPIView)
router.register('feature', FeatureAPIView)
router.register('order-item', OrderItemAPI)
router.register('order', OrderAPIView)


urlpatterns = [

    path('admin/', admin.site.urls),
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('auth/registration/confirmation-send', ConfirmationSent.as_view(), name='account_email_verification_sent'),
    path('import_price/', ImportProductsView.as_view()),
    path('/'.join([API_BASE_URL, API_VERSION[1]]), include(router.urls)),
    # SWAGGER #
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
