import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import requests
from .serializers import ChatCreateSerializer
from .models import Room, Chat, Attachment, UserMessage
import logging
logger = logging.getLogger('django')

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        room = text_data_json['room']
        user = text_data_json['user']
        message = text_data_json['message']
        _file = text_data_json['file']
        
        payload = {
            'room': room,
            'user': user,
            'text': message,
            'attachment': _file
        }
        chat = ChatCreateSerializer(data=payload)
        if chat.is_valid():
            chat.save()
        else:
            logger.warning('not valid')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'file': _file,
                'message': message,
                'user': user,
                'room': room,
            }
        )

    def chat_message(self, event):
        message = event['message']
        room = event['room']
        user = event['user']
        _file = event['file']
        attachments_info = []
        if _file:
            if str(_file).isdigit():
                message_obj = Chat.chat_attachment.get(pk=int(_file))
                attachments = message_obj.attachment.all()
                for attachment in attachments:
                    if attachment.attachment and hasattr(attachment.attachment, 'url'):
                        path_file = attachment.attachment.url
                        file_url = 'https://{domain}{path}'.format(
                            domain='mobile.turancoin.net', path=path_file)
                        attachments_info.append(
                            {
                                "file_type": attachment.attachment_type,
                                "file_url": file_url,
                            }
                        )
                    else:
                        file_url = None

        self.send(text_data=json.dumps({
            "room": room,
            "user": user,
            'message': message,
            'file': attachments_info if any(attachments_info) else []
        }))
