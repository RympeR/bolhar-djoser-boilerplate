from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from mptt.admin import DraggableMPTTAdmin, TreeRelatedFieldListFilter

from .models import (
    Card,
    Category,
    Comment,
    DelieverChoice,
    PaymentChoice,
    ProductBrand,
    ProductCountry,
    Rate,
    ShopComment,
    ShopRate,
    Shop,
    OrderItem,
    Address,
    Coupon,
    Order,
)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = 'owner', 'name', 'admin_preview'
    list_display_links = 'name',
    filter_horizontal = 'schedule',
    search_fields = 'owner__username', 'owner__fio'


@admin.register(ProductBrand, ProductCountry)
class ProductParamAmin(admin.ModelAdmin):
    list_display = 'title',
    list_display_links = 'title',
    search_fields = 'title',


@admin.register(Comment, ShopComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'comment',
        'datetime',
    )
    search_fields = ('user__username', 'user__fio',)
    list_filter = (
        ('datetime', DateFieldListFilter),
    )


@admin.register(Rate, ShopRate)
class RateAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'rate',
    )
    search_fields = ('user__username', 'user__fio',)


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'name', 'display', 'admin_preview')
    list_display_links = ('name',)
    filter_fields = ('display')
    search_fields = ('name',)
    list_filter = (
        ('parent', TreeRelatedFieldListFilter),
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'admin_preview',
        'seller',
        'present',
        'price'
    )
    list_display_links = 'title',
    search_fields = ('seller__username', 'seller__fio',)
    list_filter = (
        ('category', TreeRelatedFieldListFilter),
        'payment_methods',
        'deliver_methods'
    )
    filter_horizontal = (
        'attachments',
        'payment_methods',
        'deliver_methods',
    )


@admin.register(PaymentChoice, DelieverChoice)
class InfoAdmin(admin.ModelAdmin):
    list_display = 'name',
    list_display_links = 'name',
    search_fields = 'name',


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'ordered',
        'being_delivered',
        'received',
        'refund_requested',
        'refund_granted',
        'address',
        'coupon',
    ]
    list_display_links = [
        'address',
        'coupon'
    ]
    list_filter = ['ordered',
                   'being_delivered',
                   'received',
                   'refund_requested',
                   'refund_granted']
    search_fields = [
        'ref_code'
    ]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'street_address',
        'apartment_address',
    ]
    search_fields = ['street_address', 'apartment_address']


admin.site.register(OrderItem)
admin.site.register(Coupon)
