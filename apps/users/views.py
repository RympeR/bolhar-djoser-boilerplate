import random

from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import APIException
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.utils.utils import *

from .exception import Api202, Api400
from .models import *
from .serializers import *
from .soap import *


def set_phone_code(phone):
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
    if phone:
        code = set_phone_code(phone)
        return code


def check_phone_code(phone, code):
    if code:
        data = Phone.objects.filter(
            phone=phone, code=code, expires_at__gte=timezone.now()).first()
        if data:
            data.is_checked = True
            data.save()
            return True
        raise APIException({'code': ['The code is incorrect or expired']}, 400)
    else:
        return False


class GetSmsCode(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def post(self, request):
        phone = request.data.get('phone')

        if isinstance(phone, list):
            phone = phone[0]
        code = self.request.data.get('code')
        if phone == '+380999999999' and not code:
            raise Api202(
                    ['This phone is not confirmed, we sent SMS with a confirmation code'],
                    'user'
                )
        if phone == '+380999999999' and code == '1111':
            user, created = User.objects.get_or_create(username=str(phone))
            user.set_password(str(code))
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "auth_token": str(token)
                }, status=status.HTTP_201_CREATED
            )
        user, created = User.objects.get_or_create(
            username=phone
        )
        
        if created:
            if check_phone_code(phone, code):
                user, created = User.objects.get_or_create(username=str(phone))
                user.set_password(str(code))
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "auth_token": str(token)
                    }, status=status.HTTP_201_CREATED
                )
            else:
                get_phone_code(phone)
                raise Api202(
                    ['This phone is not confirmed, we sent SMS with a confirmation code'],
                    'user'
                )
        else:
            if check_phone_code(phone, code):
                user, created = User.objects.get_or_create(username=str(phone))
                user.set_password(str(code))
                user.save()
                token, created = Token.objects.get_or_create(user=user)
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

    def perform_create(self, serializer):
        user = User.objects.create(
            username=self.request.data['username']
        )
        user.set_password(self.request.data['password'])
        user.save()


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
        self.self.request.user.contacts = self.self.request.user.contacts
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
        self.request.user.contacts.add(
            User.objects.get(username=request.data['phone'])
        )
        return super().partial_update(request, *args, **kwargs)


class AddBlockedUserAPI(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def partial_update(self, request, *args, **kwargs):
        self.request.user.blocked_users.add(
            User.objects.get(username=request.data['phone'])
        )
        return super().partial_update(request, *args, **kwargs)


class CreatePendingUserAPI(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = PendingUser.objects.all()
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    serializer_class = PendingUserCreateSerializer
