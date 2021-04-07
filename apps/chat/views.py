from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from .models import Room, Chat
from .serializers import *


class PostRoom(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomCreateSerializer


class GetRoom(generics.RetrieveDestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomSerializer


class PutRoom(generics.UpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomCreateSerializer


class PostChat(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer


class GetChat(generics.RetrieveDestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatSerializer


class PutChat(generics.UpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer


class GetUserRooms(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, FormParser)
    serializer_class = RoomSerializer

    def get(self, request):
        rooms = Room.objects.filter(
            creator_id=request.user).values()
        return Response(rooms)
        # results = []
        # for obj in rooms:
        #     results.append(
        #         {
        #             "id": obj.pk,
        #             "creator_id": obj.creator_id.pk,
        #             "accepter_id": obj.accepter_id.pk,
        #             "date": obj.date
        #         }
        #     )
        # return Response(
        #     {
        #         "results": results
        #     }
        # )


class GetChatMessages(APIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        objects = Chat.objects.filter(
            room=room
        ).order_by('-date')
        results = []
        domain = request.get_host()
        for obj in objects:
            try:
                path_image = obj.attachment.url
            except Exception:
                path_image = None
            if path_image:
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
