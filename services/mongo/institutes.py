from rest_framework import serializers

from services.departments.serializers import DepartmentSerializer, FacilitySerializer
from services.institutes.models import Institute, InstituteDepartment, InstituteType
from services.utils.utils import get_content_type, get_profile_media, get_short_address, get_static_data
from users.serializers import UserProfileSerializer


class InstituteTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstituteType
        fields = ('id', 'name',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return InstituteType.objects.create(**validated_data)


class InstituteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Institute
        fields = ('id', 'name', 'institute_type', 'avg_rating', 'institute_url', 'total_feed')


class AllInstituteSerializer(serializers.ModelSerializer):
    """
    Serializer for all institute listing
    """
    like = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    facility = FacilitySerializer(many=True)
    department = DepartmentSerializer(many=True)
    institute_type = serializers.SerializerMethodField()
    media = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    static = serializers.SerializerMethodField()
    established_date = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ('id', 'name', 'parent', 'institute_type', 'department', 'facility', 'established_date',
                  'address', 'media', 'avg_rating', 'total_feed', 'like', 'url', 'static')
    
    def get_institute_type(self, obj):
        if obj.institute_type:
            return InstituteTypeSerializer(obj.institute_type).data
    def get_established_date(self, obj):
        return obj.established_date
    
    def get_avg_rating(self, obj):
        return int(obj.avg_rating)
    
    def get_like(self, obj):
        return obj.votes.count()

    def get_address(self, obj):
        if obj.address:
            return get_short_address(obj.address, json_address=True)
    
    def get_url(self, obj):
        return {'web': obj.get_absolute_web_url(), 'api': obj.get_absolute_url()}
    
    def get_media(self, obj):
        if obj.is_media:
            return get_profile_media(get_content_type(obj).id, obj.id)

    def get_parent(self, obj):
        if obj.parent:
            return InstituteSerializer(obj.parent).data

    def get_static(self, obj):
        return get_static_data(obj)


class InstituteDepartmentSerializer(serializers.ModelSerializer):
    """
    To add instituteDepartment data and retrieve data
    """
    user = UserProfileSerializer(many=True)
    department = serializers.SerializerMethodField()

    class Meta:
        model = InstituteDepartment
        fields = ('id', 'department', 'owner', 'user',)

    def get_department(self, obj):
        return DepartmentSerializer(obj.department).data
    
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return InstituteDepartment.objects.create(**validated_data)
