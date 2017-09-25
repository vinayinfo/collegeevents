from django.conf.urls import include, url

from rest_framework import routers

from services.commons.views import UserParticipateView

router = routers.DefaultRouter()
router.register(r'participant', UserParticipateView, base_name='participant')

urlpatterns = [
    url(r'^', include(router.urls)),
]
