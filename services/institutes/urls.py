from django.conf.urls import include, url

from rest_framework import routers

from services.institutes.views import InstituteTypeViewSet, InstituteViewSet

router = routers.SimpleRouter()
router.register(r'institute', InstituteViewSet, base_name='institute')
router.register(r'institute_type', InstituteTypeViewSet, base_name='institute_type')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^institute/(?P<id>[\w-]+)/', include('services.events.urls')),
    url(r'^institute/(?P<id>[\w-]+)/', include('services.departments.urls')),
]
