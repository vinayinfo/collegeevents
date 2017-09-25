from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from rest_framework import status
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response

from services.feeds.models import Feed
from services.feeds.serializers import FeedCreateSerializer, FeedSerializer
from services.utils.utils import add_rating, get_object_or_none


class FeedViewSet(ListCreateAPIView):
    """
    fetch all child node of parent feed
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = ()
    
    def get(self, request, *args, **kwargs):
         
        feed = self.get_object()
        queryset = self.queryset.filter(parent=feed)
  
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
  
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        self.serializer_class = FeedCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        content_type = get_object_or_none(ContentType, model=request.data.get('content_type'))
        if content_type:
            request.data['from_user'] = None if request.data['from_user']=='true' else request.user.id
            request.data['user'] = None if request.data['from_user']=='true' else request.user 
            request.data['content_type'] = content_type.id
            if request.data.get('media_ids'):
                request.data['is_media'] = True
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            add_rating(serializer.instance, self.request.user, 'feed', self.request.data)


class FeedListViewSet(ListAPIView):
    """
    fetch all child node of parent feed
    """
    queryset = Feed.objects.all()
    serializer_class = FeedSerializer
    permission_classes = ()
    
    def get(self, request, *args, **kwargs):
        content_type = get_object_or_none(ContentType, model=kwargs.get('content_type'))
        queryset = self.queryset.filter(object_id=kwargs.get('object_id'), content_type=content_type).order_by('-updated_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
