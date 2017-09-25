from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.utils.mixins import ActionRatingFeedMixin
from services.utils.utils import get_object_or_none, rate_instance
from users.models import UserProfile
from users.serializers import UserProfileSerializer, UserSerializer


class UserProfileViewSet(ActionRatingFeedMixin, ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    serializer_action_classes = {'create': UserSerializer,}
    permission_classes = ''

    @detail_route(methods='PATCH')
    def user_rating(self, request, *args, **kwargs):
        instance = get_object_or_none(UserProfile, id=kwargs.get('pk'))
        score = request.data.get('score')
        if request.user != instance:
            if rate_instance(self, self.request.user, instance, score):
                return Response('Rating added', status=status.HTTP_201_CREATED)
        return Response('Something went wrong', status=status.HTTP_400_BAD_REQUEST)
