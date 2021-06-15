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
)


@admin.register(ProductBrand, ProductCountry)
class ProductParamAmin(admin.ModelAdmin):
    list_display = 'title',
    list_display_links = 'title',
    search_fields = 'title',


@admin.register(Comment)
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


@admin.register(Rate)
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
