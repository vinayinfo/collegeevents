from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers

from services.commons.models import UserParticipate
from services.utils.utils import get_object_or_none


class UserParticipateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserParticipate

    def to_internal_value(self, data):
        data["content_type"] = get_object_or_none(ContentType, model=data.get("content_type")).id
        data["user"] = self.context.get('request').user.id
        return super(UserParticipateSerializer, self).to_internal_value(data)
