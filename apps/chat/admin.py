from django.contrib import admin
from .models import Room, Chat, Attachment

# Register your models here.
admin.site.register(Room)
admin.site.register(Chat)
admin.site.register(Attachment)
