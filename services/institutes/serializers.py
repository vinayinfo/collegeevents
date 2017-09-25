import random

from rest_framework import serializers

from services.address.serializers import AddressSerializer
from services.departments.serializers import DepartmentSerializer, FacilitySerializer
from services.institutes.models import Institute, InstituteDepartment, InstituteType
from services.utils.utils import get_short_address, get_static_data
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


class AllInstituteSerializer(serializers.ModelSerializer):
    """
    Serializer for all institute listing
    """
    like = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    institute_type = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ('id', 'name', 'parent', 'institute_type', 'established_date', 'address', 'avg_rating', 'total_feed', 'like', 'url')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Institute.objects.create(**validated_data)

    def get_avg_rating(self, obj):
        return int(obj.avg_rating)

    def get_like(self, obj):
        return obj.votes.count()

    def get_address(self, obj):
        return get_short_address(obj.address)

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_institute_type(self, obj):
        return InstituteTypeSerializer(obj.institute_type).data
    def get_parent(self, obj):
        return InstituteSerializer(obj.parent).data if obj.parent else obj.parent

class InstituteSerializer(AllInstituteSerializer):
    """
    To get single institute details
    """
    facility = FacilitySerializer(many=True)
    department = DepartmentSerializer(many=True)

    class Meta:
        model = Institute
        fields = ('id', 'name', 'parent', 'institute_type', 'facility', 'url', 'department', 'address', 'like', 'institute_url', 'established_date')


class InstituteShortSerializer(AllInstituteSerializer):
    """
    To get single institute details
    """

    class Meta:
        model = Institute
        fields = ('id', 'name', 'parent', 'institute_type', 'url', 'address', 'like', 'institute_url', 'established_date')


class InstituteStaticSerializer(AllInstituteSerializer):
    """
    To get institute Static data
    """
    static = serializers.SerializerMethodField()

    class Meta:
        model = Institute
        fields = ('id', 'name', 'parent','address',  'static',)

    def get_static(self, obj):
        return get_static_data(obj)


class InstituteDepartmentSerializer(serializers.ModelSerializer):
    """
    To add instituteDepartment data and retrieve data
    """
    department = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = InstituteDepartment
        fields = ('id', 'department', 'owner', 'url')

    def get_department(self, obj):
        return DepartmentSerializer(obj.department).data

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return InstituteDepartment.objects.create(**validated_data)

    def get_url(self, obj):
        return obj.get_absolute_url()
