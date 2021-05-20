from typing import Generic
from django.shortcuts import render
from rest_framework import generics, authentication
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
            if hasattr(obj.attachment, 'url'):
                path_image = obj.attachment.url
                image_url = 'http://{domain}{path}'.format(
                    domain=domain, path=path_image)
            else:
                image_url = None
            results.append(
                {
                    "id": obj.pk,
                    "room_id": obj.room.pk,
                    "user_id": obj.user.pk,
                    "text": obj.text,
                    "attachment": image_url,
                    "date": obj.date
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
        )[id_chat:id_chat + 15]
        room_values = list(rooms.values())
        for ind, room in enumerate(rooms):
            message = Chat.objects.filter(
                Q(room=room)
            ).order_by('-date').values().first()
            room_values[ind]['message'] = message
            room_values[ind]['message']['date'] = int(message['date'].timestamp() * 100000)
            room_values[ind]['date'] = int(room_values[ind]['date'].timestamp() * 100000)
        return Response(room_values)
