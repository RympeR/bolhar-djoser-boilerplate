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
# from .soap import *



# def set_phone(phone):
#     phone = str(phone)
#     if phone and type(phone) is not int:
#         phone = re.sub("\D", '', phone)

#         if len(phone) == 9:
#             phone = '380' + phone

#         if phone[:1] == '0':
#             phone = '38' + phone
#         if phone[:1] == '8':
#             phone = '3' + phone

#         if len(phone) == 12:
#             return int(phone)
#     return None


# def set_phone_code(phone):
#     phone = set_phone(phone)
#     if phone:
#         code = random.randint(1000, 9999)
#         Phone.objects.create(
#             phone=phone,
#             code=code,
#             expires_at=timezone.now() + relativedelta(minutes=60)
#         )
#         send_sms(phone, code)
#         return code
#     return None


# def get_phone_code(phone):
#     phone = set_phone(phone)
#     if phone:
#         sms_timeout = 1
#         switch = SettingsSwitch()
#         if sms_timeout:
#             sms_timeout = switch.dispatch(sms_timeout)
#             check = Phone.objects.filter(
#                 created_at__gte=(timezone.now() -
#                                  relativedelta(minutes=sms_timeout)),
#                 phone=phone
#             ).first()
#         sms_limit = 60
#         switch = SettingsSwitch()
#         sms_limit = switch.dispatch(sms_limit)
#         check = Phone.objects.filter(
#             created_at__gte=(timezone.now() - relativedelta(hours=1)),
#             phone=phone
#         ).count()
#         print(check)
#         code = set_phone_code(phone)

#         return code


# def check_phone_code(phone, code):
#     phone = set_phone(phone)
#     if code:
#         print(f'cpde - > {code}')
#         data = Phone.objects.filter(
#             phone=phone, code=code, expires_at__gte=timezone.now()).first()
#         if data:
#             data.is_checked = True
#             data.save()
#             return True
#         raise APIException({'code': ['The code is incorrect or expired']}, 400)
#     else:
#         return False


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return


class GetSmsCode(APIView):
    permission_classes = (permissions.AllowAny, )
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request, phone):
        acount_sid = 'AC7e26aa22e1d6d1f9439687e1959c6a67'
        acount_token = 'f79382fab3faabc4a162a6d08153637e'
        user, created = User.objects.get_or_create(
            username=phone
        )

        print(f'User->{created}')
        client = Client(acount_sid,acount_token)
        code = random.randint(1,19999)
        message =client.messages.create(
            body=str(code),
            from_='+13615416379',
            to=phone
        )
        user.set_password(str(code))
        user.save()
        return Response(
            {
                "phone": phone,
                "password": code
            }
        )

    def post(self, request):
        phone = request.data.get('phone')
    
        if isinstance(phone, list):
            phone = phone[0]
        acount_sid = 'AC7e26aa22e1d6d1f9439687e1959c6a67'
        acount_token = 'f79382fab3faabc4a162a6d08153637e'
        user, created = User.objects.get_or_create(
            username=phone
        )

        print(f'User->{created}')
        client = Client(acount_sid,acount_token)
        code = random.randint(1,19999)
        message =client.messages.create(
            body=str(code),
            from_='+13615416379',
            to=phone
        )
        user.set_password(code)
        user.save()
        return Response(
            {
                "phone": phone,
                "status": "ok"
            }
        )
        # if created:

        #     if check_phone_code(phone, code):

        #         print(f'check code->{check_phone_code(phone, code)}')
        #         token = Token.objects.create(user=user)
        #         token = Token.objects.get(user=user)

        #         return Response(
        #             {
        #                 "token": token.key
        #             }, status=status.HTTP_201_CREATED
        #         )
        #     else:       
        #         get_phone_code(phone)
        #         print(f'check code->{check_phone_code(phone, code)}')
        #         raise Api202(
        #                 ['This phone is not confirmed, we sent SMS with a confirmation code'],
        #                 'user'
        #             )
        # else:
        #     if check_phone_code(phone, code):
        #         print(f'check non reg code->{check_phone_code(phone, code)}')
        #         user = User.objects.create(phone=str(phone))
        #         user.set_password(str(code))
        #         user.save()
        #         token = Token.objects.create(user=user)
        #         token = Token.objects.get(user=user)
        #         return Response(
        #             {
        #                 "token": token.key
        #             }, status=status.HTTP_201_CREATED
        #         )
        #     else:
        #         print(f'check non reg code->{check_phone_code(phone, code)}')
        #         get_phone_code(phone)
        #         raise Api202(
        #             ['This phone is not confirmed, we sent SMS with a confirmation code'],
        #             'user'
        #         )


class CreateUserAPI(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, )
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
    
    def partial_update(self):
        self.request.user.contacts = self.request.user.contacts
        return super().partial_update(request, *args, **kwargs)

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
