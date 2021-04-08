from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.views import APIView
from .serializers import *
from .models import *
import random
from rest_framework.response import Response
from twilio.rest import Client
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class GetSmsCode(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, phone ):
        acount_sid = 'AC7e26aa22e1d6d1f9439687e1959c6a67'
        acount_token = 'dbe920a4d7f4f96ded9394435749bb14'
        client = Client(acount_sid,acount_token)
        code = random.randint(1,19999)
        message =client.messages.create(
            body=str(code),
            from_='+13615416379',
            to=phone
        )
        user, created = User.objects.get_or_create(
            username=phone
        )
        user.set_password(str(code))
        user.save()
        return Response(
            {
                "user_id": user.pk,
                "new_user": created
            }
        )
class CreateUserAPI(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserCreateSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class GetUserAPI(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = GetUserSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        return self.request.user


class UserAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        return self.request.user


class UserListAPI(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

class AddContactAPI(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        request.user.contacts.add(
            User.objects.get(username=request.data['phone'])
        )
        return super().partial_update(request, *args, **kwargs)
