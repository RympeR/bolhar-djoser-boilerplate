from django.db import models
from apps.users.models import User
from unixtimestampfield.fields import UnixTimeStampField

FILE_TYPES = (
    ('image', 'image'),
    ('video', 'video'),
    ('audio', 'audio'),
)


class Room(models.Model):

    creator_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='request_chat')
    accepter_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='proposition_chat')
    date = UnixTimeStampField(
        "Дата создания", auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'

class Chat(models.Model):
    room = models.ForeignKey(Room, verbose_name='Комната',
                             related_name='chat_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='user_sender', on_delete=models.CASCADE)
    text = models.TextField("Message", max_length=500, null=True, blank=True)
    date = UnixTimeStampField(
        "Send datetime", auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-date']


class Attachment(models.Model):
    chat = models.ForeignKey(Chat,
        verbose_name='Сообщение',  related_name='chat_attachment', null=True, blank=True, on_delete=models.DO_NOTHING)
    attachment = models.FileField("Файл", null=True, blank=True)
    attachment_type = models.CharField(
        'Тип файла', null=False, default='image', max_length=15, choices=FILE_TYPES)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'
