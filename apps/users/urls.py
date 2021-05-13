from django.urls import path
from .views import *

urlpatterns = [
    path('get-user/', GetUserAPI.as_view(), name='UserFullList'),
    path('create-profile/', CreateUserAPI.as_view(), name='UserCreate'),
    path('update-profile/', UserAPI.as_view(), name='UserUpdate'),
    path('delete-profile/', UserAPI.as_view(), name='UserDelete'),
    path('get-users-list', UserListAPI.as_view(), name='UsersFilterList'),
    path('add-contact', AddContactAPI.as_view(), name='AddContact'),
    path('sms-code/', GetSmsCode.as_view(), name='login'),
]
