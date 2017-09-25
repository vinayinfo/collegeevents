from django.conf.urls import include, url

from rest_framework import routers

from users.views import UserProfileViewSet

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
