from rest_framework import serializers
from .models import Room, Chat
from apps.users.serializers import UserSerializer


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()

    def to_internal_value(self, value):
        return value

class RoomSerializer(serializers.ModelSerializer):
    
    creator_id = UserSerializer()
    accepter_id = UserSerializer()
    date = TimestampField(required=False)

    class Meta:
        model = Room
        fields = '__all__'


class RoomCreateSerializer(serializers.ModelSerializer):
    date = TimestampField(required=False)

    class Meta:
        model = Room
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    date = TimestampField(required=False)
    user = UserSerializer()
    room = RoomSerializer()
    class Meta:
        model = Chat
        fields = '__all__'

class ChatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ('date', )
