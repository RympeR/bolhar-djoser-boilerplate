from admin_actions.admin import ActionsModelAdmin
from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from .models import PendingUser, Phone, User


def set_value(pdUser: PendingUser, value: bool, request):
    pdUser.verified = value
    pdUser.user.verified = value
    pdUser.save()
    pdUser.user.save()
    return HttpResponseRedirect(reverse_lazy('admin:users_pendinguser_changelist'), request)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'pk',
        'username',
        'user_photo',
        'fio',
        'customer',
        'verified',
        'top_seller',
    )
    list_display_links = 'pk', 'username',
    list_filter = 'customer', 'verified',
    filter_horizontal = 'blocked_users', 'contacts',
    search_fields = 'username', 'fio'
    fieldsets = (
        ('Личная информация', {
            'fields':  ('username', 'image', 'fio',)
        }
        ),
        ('Чат', {
            'fields':  ('contacts', 'blocked_users')
        }
        ),
        ('Магазин', {
                'fields': ('customer', 'verified', 'top_seller')
            }
         )
    )


@admin.register(PendingUser)
class PendingUserAdmin(ActionsModelAdmin):

    list_display = 'pk', 'user', 'user_docs', 'verified'
    list_display_links = 'pk',
    list_filter = 'verified',
    search_fields = 'user__username', 'user__fio'
    actions_row = actions_detail = 'confirm_user', 'reject_user',

    def confirm_user(self, request, pk):
        pdUser = PendingUser.objects.get(pk=pk)
        if pdUser.user.verified:
            messages.error(
                request, 'User is already verified')
            return HttpResponseRedirect(reverse_lazy('admin:users_pendinguser_changelist'), request)
        else:
            messages.success(
                request, 'User verified')
            return set_value(pdUser, True, request)

    def reject_user(self, request, pk):
        pdUser = PendingUser.objects.get(pk=pk)
        if not pdUser.user.verified:
            messages.error(
                request, 'User is not verified')
            return HttpResponseRedirect(reverse_lazy('admin:users_pendinguser_changelist'), request)
        else:
            messages.success(
                request, 'User rejected')
            return set_value(pdUser, False, request)

    confirm_user.short_description = 'Confirm'
    reject_user.short_description = 'Reject'
    confirm_user.url_path = 'confirm-pending-user'
    reject_user.url_path = 'reject-pending-user'


admin.site.register(Phone)
