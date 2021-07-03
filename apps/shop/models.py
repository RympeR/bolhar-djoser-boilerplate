from django.db import models
from django.core import validators
from django.db.models import CheckConstraint, F, Q
from django.db.models.aggregates import Avg
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


class Schedule(models.Model):
    day = models.CharField(max_length=255, verbose_name='День')
    work_time = models.CharField(max_length=255, verbose_name='Время работы')

    class Meta:
        verbose_name = 'Время работы магазина'
        verbose_name_plural = 'Время работы магазинов'

    def __str__(self):
        return self.day, ' -- ', self.work_time


class Shop(models.Model):
    owner = models.OneToOneField(User, related_name='shop_owner',
                              verbose_name='Владелец', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название')
    logo = ProcessedImageField(
        verbose_name='Логотип',
        upload_to=preview_cards,
        processors=[ResizeToFill(120, 120)],
        options={'quality': 100})
    schedule = models.ManyToManyField(Schedule,
                                      related_name='shop_schedule',
                                      verbose_name='Время работы',
                                      blank=True)
    description = models.TextField(verbose_name='Описание')

    def admin_preview(self):
        if hasattr(self.logo, 'url') and self.logo:
            return mark_safe('<img src="{}" width="100" /'.format(self.logo.url))
        return None

    def average_rate(self):
        return (
            self.shop_rate.all().aggregate(Avg('rate')) if self.shop_rate.all() else 0
        )
    admin_preview.short_description = 'Превью'
    admin_preview.allow_tags = True

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


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
        Shop, related_name='card_creator', verbose_name='Магазин продавца', on_delete=models.CASCADE,)
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
        verbose_name = 'Комментарий товара'
        verbose_name_plural = 'Комментарии товара'


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
        verbose_name = 'Оценка товара'
        verbose_name_plural = 'Оценки товара'


class ShopComment(models.Model):
    user = models.ForeignKey(
        User, related_name='user_comment_shop', verbose_name='Комментатор', null=True, on_delete=models.SET_NULL,)
    card = models.ForeignKey(Card, related_name='shop_comment', blank=True,
                             null=True, on_delete=models.CASCADE, verbose_name='Комментируемый магазин')
    comment = models.TextField(verbose_name='Комментарий')
    datetime = UnixTimeStampField(
        verbose_name="Время комментария", auto_now_add=True)

    def __str__(self):
        return f'{self.user}--{self.comment}'

    class Meta:
        verbose_name = 'Комментарий магазина'
        verbose_name_plural = 'Комментарии магазина'


class ShopRate(models.Model):

    user = models.ForeignKey(
        User, related_name='user_rate_shop', verbose_name='Оценщик', null=True, on_delete=models.SET_NULL,)
    shop = models.ForeignKey(Shop, related_name='shop_rate', blank=True,
                             null=True, on_delete=models.CASCADE, verbose_name='Оцениваемый магазин')
    rate = models.IntegerField(
        verbose_name='Оценка', validators=[validators.MinValueValidator(1), validators.MaxValueValidator(5)]
    )

    def __str__(self):
        return f'{self.user}--{self.rate}'

    class Meta:
        verbose_name = 'Оценка магазина'
        verbose_name_plural = 'Оценки магазина'


class OrderItem(models.Model):
    item = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.IntegerField('Количество', default=1)

    class Meta:
        verbose_name = 'Продукт в заказе'
        verbose_name_plural = 'Продукты в заказе'

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Address(models.Model):
    street_address = models.CharField('Улица', max_length=100)
    apartment_address = models.CharField('Квартира', max_length=100)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return str(self.sessionOrder)


class Coupon(models.Model):
    code = models.CharField('Код', max_length=15)
    discount_percent = models.IntegerField('Процент скидки')
    amount = models.IntegerField('Количество использований')

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.code


class Order(models.Model):
    user = models.ForeignKey(User, related_name='order_user',
                             verbose_name='Клиент', on_delete=models.SET_NULL, null=True)
    approved = models.BooleanField('Подтвержден', null=True, default=False)
    items = models.ManyToManyField(
        OrderItem, related_name='order_items', verbose_name='Продукты в заказе')
    fio = models.CharField('Фио', max_length=50, blank=False, null=True)
    phone_number = models.CharField(
        'Номер телефона', max_length=40, blank=False, null=True)
    email = models.EmailField('Почта', blank=True, null=True)
    ordered = models.BooleanField('Заказан', default=False)
    address = models.ForeignKey(
        Address, related_name='shipping_address', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.CharField(
        'комментарий', max_length=255, null=True, blank=True)
    being_delivered = models.BooleanField('Был доставлен', default=False)
    received = models.BooleanField('Товар получен', default=False)
    refund_requested = models.BooleanField('Возврат запрошен', default=False)
    refund_granted = models.BooleanField('Возврат выполнен', default=False)
    created_at = UnixTimeStampField('Время заказа', auto_now_add=True)
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.user}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= total*(self.coupon.discount_percent / 100)
        return total
