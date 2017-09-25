from django.conf.urls import include, url

from rest_framework import routers

from services.departments.views import DepartmentViewSet

router = routers.SimpleRouter()
router.register(r'departments', DepartmentViewSet, base_name='departments')
urlpatterns = [
    url(r'^', include(router.urls)),
]
