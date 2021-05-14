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
from .soap import *
from apps.utils.utils import *
import re
import random
from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework import status
from .exception import Api202, Api400
from rest_framework.authtoken.models import Token
from .soap import *
from apps.utils.utils import *
import requests
from rest_framework.authentication import TokenAuthentication

def set_phone(phone):
    phone = str(phone)
    if phone and type(phone) is not int:
        phone = re.sub("\D", '', phone)

        if len(phone) == 9:
            phone = '380' + phone

        if phone[:1] == '0':
            phone = '38' + phone
        if phone[:1] == '8':
            phone = '3' + phone

        if len(phone) == 12:
            return int(phone)
    return None


def set_phone_code(phone):
    phone = set_phone(phone)
    if phone:
        code = random.randint(1000, 9999)
        Phone.objects.create(
            phone=phone,
            code=code,
            expires_at=timezone.now() + relativedelta(minutes=60)
        )
        send_sms(phone, code)
        return code
    return None


def get_phone_code(phone):
    phone = set_phone(phone)
    if phone:
        sms_timeout = 1
        switch = SettingsSwitch()
        if sms_timeout:
            sms_timeout = switch.dispatch(sms_timeout)
            check = Phone.objects.filter(
                created_at__gte=(timezone.now() -
                                 relativedelta(minutes=sms_timeout)),
                phone=phone
            ).first()
        sms_limit = 60
        switch = SettingsSwitch()
        sms_limit = switch.dispatch(sms_limit)
        check = Phone.objects.filter(
            created_at__gte=(timezone.now() - relativedelta(hours=1)),
            phone=phone
        ).count()
        print(check)
        code = set_phone_code(phone)

        return code


def check_phone_code(phone, code):
    phone = set_phone(phone)
    if code:
        print(f'cpde - > {code}')
        data = Phone.objects.filter(
            phone=phone, code=code, expires_at__gte=timezone.now()).first()
        print(data)
        if data:
            data.is_checked = True
            data.save()
            return True
        raise APIException({'code': ['The code is incorrect or expired']}, 400)
    else:
        return False


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class GetSmsCode(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    
    def post(self, request):
        phone = request.data.get('phone')

        if isinstance(phone, list):
            phone = phone[0]
        user, created = User.objects.get_or_create(
            username=phone
        )

        print(f'User->{created}')
        code = self.request.data.get('code')
        print(created)
        if created:

            if check_phone_code(phone, code):

                print(f'check code->{check_phone_code(phone, code)}')
                user, created = User.objects.get_or_create(username=str(phone))
                user.set_password(str(code))
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                return Response(
                    {
                        "auth_token": str(token)
                    }, status=status.HTTP_201_CREATED
                )
            else:
                get_phone_code(phone)
                print(f'check code->{check_phone_code(phone, code)}')
                raise Api202(
                    ['This phone is not confirmed, we sent SMS with a confirmation code'],
                    'user'
                )
        else:
            if check_phone_code(phone, code):
                print(f'check non reg code->{check_phone_code(phone, code)}')
                user, created = User.objects.get_or_create(username=str(phone))
                user.set_password(str(code))
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                print(token)
                return Response(
                    {
                        "auth_token": str(token)
                    }, status=status.HTTP_201_CREATED
                )
            else:
                print(f'check non reg code->{check_phone_code(phone, code)}')
                get_phone_code(phone)
                raise Api202(
                    ['This phone is not confirmed, we sent SMS with a confirmation code'],
                    'user'
                )


class CreateUserAPI(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserCreateSerializer
   
class GetUserAPI(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = GetUserSerializer


    def get_object(self):
        print(self.request.user.username)
        return self.request.user


class UserAPI(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer

    def get_object(self):
        print(self.request.user)
        return self.request.user

    def partial_update(self, *args, **kwargs):
        self.request.user.contacts = self.request.user.contacts
        return super().partial_update(self.request, *args, **kwargs)


class UserListAPI(generics.ListAPIView):
    permission_classes = (permissions.AllowAny, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer
    

class AddContactAPI(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        request.user.contacts.add(
            User.objects.get(username=request.data['phone'])
        )
        return super().partial_update(request, *args, **kwargs)
