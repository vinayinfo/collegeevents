from django.conf.urls import include, url

from rest_framework import routers

from services.events.views import InstituteEventsViewSet

router = routers.SimpleRouter()
router.register(r'events', InstituteEventsViewSet)

urlpatterns = [
               url(r'^', include(router.urls)),
               ]
