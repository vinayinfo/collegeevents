from django.conf.urls import include, url

from services.feeds.views import FeedListViewSet, FeedViewSet

urlpatterns = [
    url(r'^feeds/(?P<content_type>[\w-]+)/(?P<object_id>[\w-]+)/$', FeedListViewSet.as_view(), name='feed-list'),
    url(r'^feed/(?P<pk>[\w-]+)/$', FeedViewSet.as_view(), name='child-feed-list'),
    url(r'^feed/$', FeedViewSet.as_view(), name='feed-save'),
]
