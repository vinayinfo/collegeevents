from django.db import transaction

from rest_framework.viewsets import ModelViewSet

from services.celerytasks.events import update_event
from services.events.models import Events
from services.events.serializers import EventsSerializer
from services.feeds.serializers import FeedSerializer
from services.utils.mixins import ActionRatingFeedMixin
from services.utils.utils import add_media


class InstituteEventsViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    self_class = Events
    serializer_action_classes = {'feeds': FeedSerializer, }

    def get_queryset(self):
        queryset = self.queryset
        if self.kwargs.get('id'):
            queryset = queryset.filter(institute__id=self.kwargs.get('id')).order_by('-updated_at')
        return queryset

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()
            media_id = self.request.data.get('media_id')
            if media_id:
                add_media([media_id], serializer.instance, category='event-profile', user=self.request.user)
        update_event.delay(str(serializer.instance.id))

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save()
            media_id = self.request.data.get('media_id')
            if media_id:
                add_media([media_id], serializer.instance, category='event-profile', user=self.request.user)
        update_event.delay(str(serializer.instance.id))

    def perform_destroy(self, instance):
        instance.delete()
        update_event.delay(str(instance.id), delete=True)

class EventsViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    self_class = Events
    serializer_action_classes = {'feeds': FeedSerializer, }

    def get_queryset(self):
        return self.queryset.order_by('-avg_rating')

    def perform_update(self, serializer):
        with transaction.atomic():
            serializer.save()
            media_id = self.request.data.get('media_id')
            if media_id:
                add_media([media_id], serializer.instance, category='event-profile', user=self.request.user)
