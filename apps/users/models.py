import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.aggregates import Avg
from django.utils.safestring import mark_safe
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from unixtimestampfield.fields import UnixTimeStampField

from apps.utils.func import user_avatar


class User(AbstractUser):
    username = models.CharField(
        'Телефон',
        unique=True,
        max_length=20
    )
    fio = models.CharField('ФИО', max_length=255, null=True, blank=True)
    
    image = ProcessedImageField(
        verbose_name='ImagePNG',
        processors=[ResizeToFill(600, 600)],
        options={'quality': 100},
        upload_to=user_avatar,
        null=True,
        blank=True
    )

    contacts = models.ManyToManyField(
        'self',
        blank=True,
        related_name='user_contacts'
    )
    
    blocked_users = models.ManyToManyField(
        'self',
        blank=True,
        related_name='blocked_contacts'
    )
    
    customer = models.BooleanField(verbose_name='Продавец', default=False)
    verified = models.BooleanField(verbose_name='Верифицирован', default=False)
    top_seller = models.BooleanField(verbose_name='Купил место', default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
    ]

    def get_average_rate(self):
        return (
            self.shop_owner.average_rate if self.shop_owner else 0
        )

    def user_photo(self):
        if self.image and hasattr(self.image, 'url'):
            return mark_safe('<img src="{}" width="100" /'.format(self.image.url))
        return None

    def get_contacts(self):
        return ' || '.join(self.contacts.all())
    
    def get_blocked_users(self):
        return ' || '.join(self.blocked_users.all())

    @staticmethod
    def _create_user( password, **extra_fields):
        user = User.objects.create(
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_user(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(password,  **extra_fields)

    def create_superuser(self, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(password,  **extra_fields)

    def __str__(self):
        return str(self.username)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Phone(models.Model):
    phone = models.CharField(max_length=20, db_index=True)
    code = models.IntegerField('Code', db_index=True)
    is_checked = models.BooleanField('Is checked', default=False)
    created_at = models.DateTimeField('Created at', auto_now=True)
    expires_at = models.DateTimeField('Expires at', default=datetime.date.today() + relativedelta(minutes=20))

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'

class PendingUser(models.Model):
    user = models.ForeignKey(User, related_name='penging_user', verbose_name='Пользователь', on_delete=models.CASCADE)
    docs = ProcessedImageField(
        verbose_name='Фото документов',
        processors=[ResizeToFill(600, 600)],
        options={'quality': 100},
        null=True,
        blank=True
    )
    verified = models.BooleanField(verbose_name='Верифицирован', default=False)

    def user_docs(self):
        if hasattr(self.docs, 'url'):
            return mark_safe('<img src="{}" width="100" /'.format(self.docs.url))
        return None


    class Meta:
        verbose_name = 'PendingUser'
        verbose_name_plural = 'PendingUsers'
