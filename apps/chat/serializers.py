from rest_framework import serializers
from .models import Room, Chat, Attachment
from apps.users.serializers import UserSerializer, UserShortSerializer


class AttachmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attachment
        fields = '__all__'


class TimestampField(serializers.Field):
    def to_representation(self, value):
        return value.timestamp()

    def to_internal_value(self, value):
        return value


class RoomSerializer(serializers.ModelSerializer):

    creator_id = UserShortSerializer()
    accepter_id = UserShortSerializer()
    date = TimestampField(required=False)

    class Meta:
        model = Room
        fields = '__all__'

class RoomShortSerializer(serializers.ModelSerializer):

    creator_id = UserShortSerializer()
    accepter_id = UserShortSerializer()
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
    user = UserShortSerializer()
    room = RoomSerializer()
    attachment = AttachmentSerializer(many=True)

    class Meta:
        model = Chat
        fields = '__all__'


class ChatCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        exclude = ('date', )

class ChatRoomSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(required=False)
