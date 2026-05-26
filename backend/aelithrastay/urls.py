"""
URL configuration for aelithrastay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, UserViewSet
from bookings.views import BookingViewSet
from notifications.views import NotificationViewSet
from payments.views import PaymentViewSet
from properties.views import AmenityViewSet, PropertyImageViewSet, PropertyViewSet
from reviews.views import ReviewViewSet
from wishlist.views import WishlistViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('amenities', AmenityViewSet, basename='amenity')
router.register('properties', PropertyViewSet, basename='property')
router.register('property-images', PropertyImageViewSet, basename='property-image')
router.register('bookings', BookingViewSet, basename='booking')
router.register('payments', PaymentViewSet, basename='payment')
router.register('reviews', ReviewViewSet, basename='review')
router.register('wishlist', WishlistViewSet, basename='wishlist')
router.register('notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
