# Generated by Django 3.1.8 on 2021-05-14 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0002_auto_20210407_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='chat',
        ),

        migrations.AddField(
            model_name='chat',
            name='attachment',
            field=models.ManyToManyField(related_name='chat_attachment', to='chat.Attachment'),
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('readed', models.BooleanField(default=False)),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivered_message', to='chat.chat', verbose_name='Доставленное сообщение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination_user', to=settings.AUTH_USER_MODEL, verbose_name='Конечный пользователь')),
            ],
            options={
                'verbose_name': 'Статус сообщения',
                'verbose_name_plural': 'Статусы сообщений',
                'ordering': ['-message__date'],
            },
        ),
    ]
