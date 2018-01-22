from django.conf import settings
from django.conf.urls import include, url, handler404
from django.contrib import admin
from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_nested import routers

from rest_core import views


router = routers.SimpleRouter()
router.register(r'user', views.UserViewSet)

users_router = routers.NestedSimpleRouter(router, r'user', lookup='user')
users_router.register(r'trips', views.TripViewSet, base_name='user-trips')


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^teslooptest/', include(router.urls)),
    url(r'^teslooptest/', include(users_router.urls)),
    url(r'^teslooptest/rest-auth/', include('rest_auth.urls')),
    url(r'^teslooptest/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^teslooptest/refresh-token/', refresh_jwt_token),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

handler404 = views.error_404