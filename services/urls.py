"""myschoolmycollege URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url

from rest_framework import routers

from services.events.views import EventsViewSet

router = routers.SimpleRouter()
router.register(r'events', EventsViewSet)

urlpatterns = [
    url(r'^', include('users.urls')),
    url(r'^', include('services.institutes.urls')),
    url(r'^', include('services.feeds.urls')),
    url(r'^', include('services.commons.urls')),
    url(r'^', include(router.urls)),
#     url(r'^q/', include('services.quiz.urls')),
]
