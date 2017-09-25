from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from services.utils.utils import get_all_feeds, get_all_users, search_data

from .utils import get_object_or_none, rate_instance


class ActionRatingFeedMixin(object):

    def _pagination(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(ActionRatingFeedMixin, self).get_serializer_class()

    @detail_route(methods=['post'], url_path='rating')
    def user_rating(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_none(self.self_class, id=pk)
        score = int(request.data.get('score', 0))
        if rate_instance(self.request, self.request.user, instance, score):
            return Response('Rating added', status=status.HTTP_201_CREATED)
        return Response('Something went wrong', status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['get'], url_path='feeds')
    def feeds(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_none(self.self_class, id=pk)
        queryset = get_all_feeds(instance)
        self._pagination(queryset)

    @detail_route(methods=['get'], url_path='static-data')
    def static_data(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_none(self.self_class, id=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['get'], url_path='users')
    def users(self, request, pk=None, *args, **kwargs):
        instance = get_object_or_none(self.self_class, id=pk)
        queryset = get_all_users(instance)
        self._pagination(queryset)

    @list_route(methods=['get'], url_path='search')
    def search(self, request, pk=None, *args, **kwargs):
        queryset = search_data(self.self_class, **request.query_params.dict())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
