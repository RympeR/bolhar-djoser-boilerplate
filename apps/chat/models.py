from django.db import models
from apps.users.models import User
from unixtimestampfield.fields import UnixTimeStampField
from django.db.models.signals import post_save

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


class Attachment(models.Model):
    attachment = models.FileField("Файл", null=True, blank=True)
    attachment_type = models.CharField(
        'Тип файла', null=False, default='image', max_length=15, choices=FILE_TYPES)

    class Meta:
        verbose_name = 'Вложение'
        verbose_name_plural = 'Вложения'


class Chat(models.Model):
    room = models.ForeignKey(Room, verbose_name='Комната',
                             related_name='chat_room', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь',
                             related_name='user_sender', on_delete=models.CASCADE)
    text = models.TextField("Message", max_length=500, null=True, blank=True)
    date = UnixTimeStampField(
        "Send datetime", auto_now_add=True, null=True, blank=True)
    attachment = models.ManyToManyField(
        Attachment, related_name='chat_attachment')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-date']


class UserMessage(models.Model):
    message = models.ForeignKey(Chat, verbose_name='Доставленное сообщение',
                                related_name='delivered_message', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='destination_user',
                             verbose_name='Конечный пользователь', on_delete=models.CASCADE)
    readed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Статус сообщения'
        verbose_name_plural = 'Статусы сообщений'
        ordering = ['-message__date']

    def __str__(self):
        return f"{self.message}-{self.user}"


def create_message(sender, instance, created, **kwargs):
    if created:
        room = instance.room
        if room.creator_id.pk != instance.user.pk:
            user = room.creator_id
        else:
            user = room.accepter_id
        UserMessage.objects.create(
            message=instance,
            user=user
        ).save()


post_save.connect(create_message, sender=Chat)
