from rest_framework import serializers

from services.events.models import Events
from services.utils.utils import join_count, join_status


class EventsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    event_join_status = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Events
        fields = ('id', 'institute', 'department', 'name', 'description', 'fee', 'address', 'apply_date', 'count', 'apply_last_date',
                  'event_start_date', 'event_last_date', 'availability', 'tags', 'avg_rating', 'url', 'created_at', 'updated_at',
                  'event_join_status', 'is_media', 'total_feed')
        read_only_fields = ('avg_rating', 'event_join_status')
    
    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_count(self, obj):
        return join_count(obj)

    def get_event_join_status(self, obj):
        return join_status(obj, self.context.get('request').user.id)

    def get_avg_rating(self, obj):
        return int(obj.avg_rating)
