from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from rest_framework import authentication, generics, status
from rest_framework.parsers import (FileUploadParser, FormParser, JSONParser,
                                    MultiPartParser)
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat, Room
from .serializers import *


class PostRoom(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer


class GetRoom(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class PutRoom(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomCreateSerializer


class PostChat(generics.CreateAPIView):
    authentication_classes = authentication.TokenAuthentication,
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer


class GetChat(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatSerializer


class PutChat(generics.UpdateAPIView):
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer


class GetChatMessages(APIView):

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        if request.data.get('message_id'):
            objects = Chat.objects.filter(
                room=room,
                pk__lte=request.data['message_id']
            ).order_by('-date')[:15]
        else:
            objects = Chat.objects.filter(
                room=room
            ).order_by('-date')[:15]
        results = []
        domain = request.get_host()
        for obj in objects:
            attachments = obj.attachment.all()
            attachments_info = []
            for attachment in attachments:
                if attachment.attachment and hasattr(attachment.attachment, 'url'):
                    path_file = attachment.attachment.url
                    file_url = 'http://{domain}{path}'.format(
                        domain=domain, path=path_file)
                    attachments_info.append(
                        {
                            "file_type": attachment.attachment_type,
                            "file_url": file_url,
                        }
                    )
                else:
                    file_url = None
            results.append(
                {
                    "id": obj.pk,
                    "room_id": obj.room.pk,
                    "user_id": obj.user.pk,
                    "text": obj.text,
                    "attachment": attachments_info,
                    "date": int(obj.date.timestamp())
                },
            )
        return Response(
            {
                "results": results
            }
        )


def index(request):
    return render(request, 'index.html')


def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })


class GetUserRooms(generics.GenericAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get(self, request, index):
        user = request.user
        id_chat = int(index)
        rooms = Room.objects.filter(
            (Q(creator_id=user) |
            Q(accepter_id=user)) &
            Q(pk__gt=id_chat)
        )
        if rooms.exists():
            rooms = rooms[:15]
            room_values = [RoomShortSerializer(instance=room, context={'request': self.request}).data for room in rooms]
            for ind, room in enumerate(rooms):
                message = Chat.objects.filter(
                    Q(room=room)
                ).order_by('-date')[0]
                creator = room.creator_id
                accepter = room.accepter_id
                has_blocked = False
                was_blocked = False
                if creator in accepter.blocked_users.all():
                    has_blocked = True
                if accepter in creator.blocked_users.all():
                    was_blocked = True
                room_values[ind]['has_blocked'] = has_blocked
                room_values[ind]['was_blocked'] = was_blocked
                if message:
                    message = ChatSerializer(instance=message, context={'request': self.request}).data
                    room_values[ind]['message'] = message
                    room_values[ind]['message']['date'] = int(
                        message['date'] * 100000)
                room_values[ind]['date'] = int(
                    room_values[ind]['date'] * 100000) if room_values[ind].get('date') else None
            return Response(room_values)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)

    def get_serializer_context(self):
        return {'request': self.request}