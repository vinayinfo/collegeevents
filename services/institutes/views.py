from rest_framework.viewsets import ModelViewSet

from services.feeds.serializers import FeedSerializer
from services.institutes.models import Institute, InstituteType
from services.institutes.serializers import (AllInstituteSerializer, InstituteSerializer, InstituteStaticSerializer,
                                             InstituteTypeSerializer)
from services.utils.mixins import ActionRatingFeedMixin
from users.serializers import UserShortProfileSerializer


class InstituteTypeViewSet(ModelViewSet):
    queryset = InstituteType.objects.all().order_by('name')
    serializer_class = InstituteTypeSerializer


class InstituteViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = Institute.objects.all().order_by('-avg_rating')
    serializer_class = AllInstituteSerializer
    self_class = Institute
    serializer_action_classes = {'retrieve': InstituteSerializer,
                                 'feeds': FeedSerializer,
                                 'static_data': InstituteStaticSerializer,
                                 'users': UserShortProfileSerializer
                                 }
