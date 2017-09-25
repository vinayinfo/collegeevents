from rest_framework import serializers

from services.address.serializers import AddressSerializer, ShortAddressSerializer
from services.utils.utils import get_content_type, get_short_address
from users.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    """
    Full user profile data
    """
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'password',
                  'user_role', 'is_active', 'date_of_birth', 'gender', 'phone_number',
                  'address', 'last_login', 'date_joined',)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return UserProfile.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Full user profile data
    """
    full_name = serializers.SerializerMethodField()
    user_role = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'full_name', 'email', 'user_role', 'is_active', 'date_of_birth', 'gender',
                  'phone_number', 'address', 'last_login', 'date_joined')
        read_only_fields = ('id', 'is_active', 'last_login', 'date_joined')

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_user_role(self, obj):
        try:
            return obj.user_role.name
        except:
            return

    def get_address(self, obj):
        return AddressSerializer(obj.address).data


class UserShortProfileSerializer(UserProfileSerializer):
    """
    Short user profile data
    """
    address = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'full_name', 'gender', 'email', 'user_role', 'date_of_birth', 'address', 'is_media')

    def get_address(self, obj):
        return get_short_address(obj.address)

    def get_gender(self, obj):
        return 'male' if obj.gender == 1 else 'female'
