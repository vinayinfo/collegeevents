from rest_framework import serializers

from services.departments.serializers import DepartmentSerializer
from services.events.models import Events
from services.institutes.serializers import InstituteShortSerializer
from services.utils.utils import get_content_type, get_profile_media, get_short_address, join_count


class EventsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    participant_count = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    institute = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    apply_date = serializers.SerializerMethodField()
    apply_last_date = serializers.SerializerMethodField()
    event_start_date = serializers.SerializerMethodField()
    event_last_date = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    
    class Meta:
        model = Events
        fields = ('id', 'institute', 'department', 'name', 'description', 'fee', 'address', 'apply_date', 'participant_count', 'apply_last_date',
                  'event_start_date', 'event_last_date', 'availability', 'tags', 'avg_rating', 'url', 'created_at', 'updated_at',
                  'total_feed', 'media')
        read_only_fields = ('avg_rating', 'event_join_status')

    def get_institute(self, obj):
        if obj.institute:
            return InstituteShortSerializer(obj.institute).data

    def get_department(self, obj):
        if obj.department:
            return DepartmentSerializer(obj.department).data

    def get_apply_date(self, obj):
        return obj.apply_date
    
    def get_apply_last_date(self, obj):
        return obj.apply_last_date
    
    def get_event_start_date(self, obj):
        return obj.event_start_date
    
    def get_event_last_date(self, obj):
        return obj.event_last_date
    
    def get_created_at(self, obj):
        return obj.created_at
    
    def get_updated_at(self, obj):
        return obj.updated_at
    
    def get_url(self, obj):
        return {'web': obj.get_absolute_web_url(), 'api': obj.get_absolute_url()}

    def get_participant_count(self, obj):
        return join_count(obj)

    def get_avg_rating(self, obj):
        return int(obj.avg_rating)

    def get_media(self, obj):
        if obj.is_media:
            return get_profile_media(get_content_type(obj).id, obj.id)
    
    def get_address(self, obj):
        if obj.address:
            return get_short_address(obj.address, json_address=True)
