from django.db import models
from django.core import validators
from django.db.models import CheckConstraint, F, Q
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel, TreeForeignKey
from unixtimestampfield.fields import UnixTimeStampField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

import jsonfield

from apps.chat.models import Attachment
from apps.users.models import User
from apps.utils.func import attachments, preview_cards


class ProductBrand(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название брэнда')


class ProductCountry(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название страны')


class Category(MPTTModel):
    parent = TreeForeignKey(
        'self', verbose_name='parent_category', blank=True, null=True, related_name='parent_category', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=100)
    display = models.BooleanField('Отобразить', default=True)
    category_image = models.ImageField(
        verbose_name='Картинка категории', blank=True, null=True)

    def admin_preview(self):
        if hasattr(self.category_image, 'url') and self.category_image:
            return mark_safe('<img src="{}" width="100" /'.format(self.category_image.url))
        return None

    admin_preview.short_description = 'Превью'
    admin_preview.allow_tags = True

    def __str__(self):
        return f"{self.name}"

    class MPTTMeta:
        order_insertion_by = ['name']
        level_attr = 'Подкатегория категории'

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class PaymentChoice(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип оплаты')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Вид оплаты'
        verbose_name_plural = 'Виды оплат'


class DelieverChoice(models.Model):
    name = models.CharField(max_length=100, verbose_name='Тип доставки')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Вид доставки'
        verbose_name_plural = 'Виды доставок'


class Card(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание товара', null=True, blank=True)
    seller = models.ForeignKey(
        User, related_name='card_creator', verbose_name='Продавец', on_delete=models.CASCADE,)
    present = models.BooleanField(default=True, verbose_name='В наличии')
    price = models.FloatField(verbose_name='Цена')
    discount_price = models.FloatField(
        verbose_name='Цена со скидкой', default=0)
    preview = ProcessedImageField(upload_to=preview_cards,
                                  processors=[ResizeToFill(100, 100)],
                                  options={'quality': 100})
    attachments = models.ManyToManyField(
        Attachment, related_name='card_attachments', verbose_name='Вложения')
    category = models.ForeignKey(
        Category, related_name='card_category', verbose_name='Категория товара', null=True, on_delete=models.SET_NULL,)
    payment_methods = models.ManyToManyField(PaymentChoice,
                                             related_name='card_payment_methods', verbose_name='Способы оплаты')
    deliver_methods = models.ManyToManyField(DelieverChoice,
                                             related_name='card_deliver_methods', verbose_name='Способы оплаты')
    characteristics = jsonfield.JSONField(verbose_name='Характеристики')

    product_brand = models.ForeignKey(ProductBrand, related_name='brand_product',
                                      verbose_name='Брэнд продукта', null=True, on_delete=models.SET_NULL, blank=True)
    product_country = models.ForeignKey(ProductCountry, related_name='country_product',
                                        verbose_name='Страна продукта', null=True, on_delete=models.SET_NULL, blank=True)

    def admin_preview(self):
        if hasattr(self.preview, 'url') and self.preview:
            return mark_safe('<img src="{}" width="100" /'.format(self.preview.url))
        return None

    admin_preview.short_description = 'Превью'
    admin_preview.allow_tags = True

    class Meta:
        constraints = [
            # CheckConstraint(
            #     check=(Q(seller__customer=True) & Q(seller__verified=True)),
            #     name='check_seller_is_Ssller',
            # ),
        ]
        verbose_name = 'Карточка товара'
        verbose_name_plural = 'Карточки товаров'


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name='comment', verbose_name='Комментатор', null=True, on_delete=models.SET_NULL,)
    card = models.ForeignKey(Card, related_name='card_comment', blank=True,
                             null=True, on_delete=models.CASCADE, verbose_name='Комментируемая карта')
    comment = models.TextField(verbose_name='Комментарий')
    datetime = UnixTimeStampField(
        verbose_name="Время комментария", auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.comment}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Rate(models.Model):

    user = models.ForeignKey(
        User, related_name='user_rate', verbose_name='Оценщик', null=True, on_delete=models.SET_NULL,)
    card = models.ForeignKey(Card, related_name='card_rate', blank=True,
                             null=True, on_delete=models.CASCADE, verbose_name='Оцениваемая карта')
    rate = models.IntegerField(
        verbose_name='Оценка', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)]
    )

    def __str__(self):
        return f'{self.user}--{self.rate}'

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'Оценки'
