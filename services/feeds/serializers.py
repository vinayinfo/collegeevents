from rest_framework import serializers

from services.feeds.models import Feed
from users.serializers import UserShortProfileSerializer


class FeedCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for feed model 
    """
    class Meta:
        model = Feed


class FeedSerializer(serializers.ModelSerializer):
    """
    Serializer for feed model 
    """
    rating = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    reply_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Feed
        fields = ('id', 'user', 'message', 'rating', 'updated_at', 'reply_count', 'like_count', 'is_media')
        read_only_fields = ('rating', 'reply_count', 'like_count')

    def get_rating(self, obj):
        if obj.from_user:
            return obj.rating.get_rating_for_user(obj.from_user)
        return obj.rating_score
    
    def get_user(self, obj):
        return UserShortProfileSerializer(obj.from_user).data

    def get_reply_count(self, obj):
        return obj.children_count
    
    def get_like_count(self, obj):
        return obj.votes.count()
