"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
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
]