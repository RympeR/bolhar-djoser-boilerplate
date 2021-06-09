from typing import Generic
from django.shortcuts import render
from rest_framework import generics, authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from .models import Room, Chat
from .serializers import *
from django.db.models import Q
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
        room = Room.objects.get(pk=room_id)
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
            if obj.attachment and hasattr(obj.attachment, 'url'):
                image_url = 'https://{domain}{path}'.format(
                    domain=domain, path=obj.attachment.url)
            else:
                image_url = None
            results.append(
                {
                    "id": obj.pk,
                    "room_id": obj.room.pk,
                    "user_id": obj.user.pk,
                    "text": obj.text,
                    "attachment": image_url,
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
            Q(creator_id=user) |
            Q(accepter_id=user)
        )
        if rooms.exists():
            rooms = rooms[id_chat:id_chat + 15]
            room_values = list(rooms.values())
            for ind, room in enumerate(rooms):
                message = Chat.objects.filter(
                    Q(room=room)
                ).order_by('-date').values().first()
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
                    room_values[ind]['message']['date'] = int(
                        message['date'].timestamp() * 100000)
                room_values[ind]['date'] = int(
                    room_values[ind]['date'].timestamp() * 100000) if room_values[ind].get('date') else None
            return Response(room_values)
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
