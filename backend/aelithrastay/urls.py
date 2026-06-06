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
from django.http import JsonResponse  # <-- Added for the root view response
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import CurrentUserView, EmailOrUsernameTokenObtainPairView, RegisterView, UserViewSet
from accounts.admin_views import AdminUserViewSet, AdminLogViewSet
from bookings.views import BookingViewSet
from bookings.admin_views import AdminDisputeViewSet
from notifications.views import NotificationViewSet
from notifications.admin_views import AdminNotificationViewSet
from payments.views import PaymentViewSet
from payments.admin_views import AdminPaymentViewSet
from properties.views import AmenityViewSet, PropertyImageViewSet, PropertyViewSet
from properties.admin_views import AdminPropertyApprovalViewSet
from reviews.views import ReviewViewSet
from reviews.admin_views import AdminReviewModerationViewSet
from wishlist.views import WishlistViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... any other paths you have like path('api/', include(...)) ...
]

# 2. ONLY append the static helper AFTER urlpatterns has been created above
if settings.MEDIA_URL:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Simple view function to handle the empty/root path
def api_root(request):
    return JsonResponse({
        "project": "AelithraStay API Backend",
        "status": "Running successfully",
        "endpoints": {
            "admin": "/admin/",
            "api_root": "/api/",
            "auth": {
                "register": "/api/auth/register/",
                "login": "/api/auth/login/",
                "refresh": "/api/auth/refresh/"
            }
        }
    })

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

# Admin routes
router.register('admin/users', AdminUserViewSet, basename='admin-user')
router.register('admin/disputes', AdminDisputeViewSet, basename='admin-dispute')
router.register('admin/reviews', AdminReviewModerationViewSet, basename='admin-review')
router.register('admin/properties', AdminPropertyApprovalViewSet, basename='admin-property')
router.register('admin/payments', AdminPaymentViewSet, basename='admin-payment')
router.register('admin/notifications', AdminNotificationViewSet, basename='admin-notification')
router.register('admin/logs', AdminLogViewSet, basename='admin-log')

urlpatterns = [
    path('', api_root, name='root_index'),  # <-- Fixed: Maps http://127.0.0.1:8000/ to the welcome view
    path('admin/', admin.site.urls),
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', EmailOrUsernameTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/me/', CurrentUserView.as_view(), name='current_user'),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
