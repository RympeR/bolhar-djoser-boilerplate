from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser, FileUploadParser
from .models import Room, Chat
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.db.models import Q

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return

class PostRoom(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomCreateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class GetRoom(generics.RetrieveDestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class PutRoom(generics.UpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = RoomCreateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class PostChat(generics.CreateAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class GetChat(generics.RetrieveDestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class PutChat(generics.UpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = Chat.objects.all()
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    serializer_class = ChatCreateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class GetUserRooms(APIView):
    permission_classes = (IsAuthenticated, )
    queryset = Room.objects.all()
    parser_classes = (JSONParser, FormParser)
    serializer_class = RoomSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

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
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
        
    def post(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        objects = Chat.objects.filter(
            room=room,
            pk__lte=request.data['message_id']
        ).order_by('-date')[:15]
        results = []
        domain = request.get_host()
        for obj in objects:
            if hasattr(obj.attachment, 'url') :
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


class GetUserRooms(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    renderer_classes = (JSONRenderer, )
    parser_classes = (JSONParser, MultiPartParser,
                      FileUploadParser, FormParser)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = Room.objects.all()
    serializer_class = RoomSerializer()

    def get_queryset(self):
        user = self.request.user
        id_chat = self.request.data['chat_id']
        rooms = Room.objects.filter(
            Q(creator_id=user) |
            Q(accepter_id=user)
        )[id_chat:id_chat + 15]
        room_values = rooms.values()
        for ind, room in enumerate(rooms):
            message = Chat.objects.filter(
                Q(room=room)
            ).order_by('-date').values()[:1]
            room_values[ind]['message'] = message
        print(room_values)
        return room_values    

