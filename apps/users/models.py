import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill
from apps.utils.func import user_avatar
from unixtimestampfield.fields import UnixTimeStampField
from dateutil.relativedelta import relativedelta
import datetime




class User(AbstractUser):
    username = models.CharField(
        'Phone',
        unique=True,
        max_length=20
    )
    fio = models.CharField('FIO', max_length=255, null=True, blank=True)
    
    image = ProcessedImageField(
        verbose_name='ImagePNG',
        processors=[ResizeToFill(600, 600)],
        options={'quality': 100},
        null=True,
        blank=True
    )

    contacts = models.ManyToManyField(
        'self',
        blank=True,
        related_name='user_contacts'
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
    ]

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
    phone = models.BigIntegerField(db_index=True)
    code = models.IntegerField('Code', db_index=True)
    is_checked = models.BooleanField('Is checked', default=False)
    created_at = models.DateTimeField('Created at', auto_now=True)
    expires_at = models.DateTimeField('Expires at', default=datetime.date.today() + relativedelta(minutes=20))

    def __str__(self):
        return str(self.phone)

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'
