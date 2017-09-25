from rest_framework import serializers

from services.address.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Address Serializer
    """
    class Meta:
        model = Address

class ShortAddressSerializer(serializers.Serializer):
    """
    Short Address Serializer
    """
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        city = state = country = ''
        try:
            city = obj.address.locality.name
        except:
            pass
        try:
            state = obj.address.locality.state.name
        except:
            pass
        try:
            country = obj.address.locality.state.country.code
        except:
            pass
        return city + ' ' + state + ' ' + country
