from rest_framework import serializers
from Users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("Id", 'Name', 'Email', 'AddressPostcode', 'StateName')
