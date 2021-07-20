from django.urls import path

from .views import *

urlpatterns = [
    path('user-rooms/<int:index>', GetUserRooms.as_view()),
    path('create-room/', PostRoom.as_view()),
    path('create-attachment/', CreateAttachment.as_view()),
    path('update-room/<int:pk>', PutRoom.as_view()),
    path('delete-room/<int:pk>', DeleteRoom.as_view()),
    path('get-room/<int:pk>', GetRoom.as_view()),
    path('create-message/', PostChat.as_view()),
    path('update-message/<int:pk>', PutChat.as_view()),
    path('delete-message/<int:pk>', GetChat.as_view()),
    path('get-message/<int:pk>', GetChat.as_view()),
    path('messages/<int:room_id>/', GetChatMessages.as_view()),
    path('', index, name='index'),
    path('<int:room_name>/', room, name='room'),
    path('last_chats/', GetUserRooms.as_view())
]