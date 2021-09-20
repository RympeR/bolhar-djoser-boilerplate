from rest_framework import serializers
from django.db.models import Avg, Count
from apps.users.serializers import (
    ShortUserSerializer,
    UserShortSerializer
)
from apps.users.models import (
    User
)
from apps.utils.customFields import TimestampField
from apps.chat.serializers import AttachmentSerializer
from .models import (
    Category,
    PaymentChoice,
    DelieverChoice,
    Comment,
    Rate,
    Card,
    Shop,
    ShopComment,
    ShopRate,
    OrderItem,
    Address,
    Coupon,
    Order,
    Schedule,
    Characteristic,
    CardCharacteristic,
    MainSlider,
    ProductBrand,
    ProductCountry,
)
from random import sample


class CategoryGetSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Category.objects.all(),)

    class Meta:
        model = Category
        fields = '__all__'


class ProductBrandGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductBrand
        fields = '__all__'


class ProductCountryGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCountry
        fields = '__all__'


class CategoryShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = 'id', 'name', 'category_image'

    def get_category_image(self, category):
        request = self.context.get('request')
        if category.category_image and getattr(category.category_image, 'url'):
            file_url = category.category_image.url
            return request.build_absolute_uri(file_url)
        return None


class MainSliderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MainSlider
        fields = '__all__'

    def get_image(self, slider):
        request = self.context.get('request')
        if slider.image and getattr(slider.image, 'url'):
            file_url = slider.image.url
            return request.build_absolute_uri(file_url)
        return None


class CharacteristicGetSerizlier(serializers.ModelSerializer):

    category = CategoryShortSerializer()

    class Meta:
        model = Characteristic
        fields = '__all__'


class CharacteristicGetShortSerizlier(serializers.ModelSerializer):

    class Meta:
        model = Characteristic
        fields = 'pk', 'name',


class CardCharacteristicGetShortSerizlier(serializers.ModelSerializer):
    characteristic = CharacteristicGetShortSerizlier()

    class Meta:
        model = CardCharacteristic
        fields = 'pk', 'value', 'characteristic'


class CardCreateSerializer(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Shop.objects.all())
    discount_price = serializers.FloatField(required=False)

    class Meta:
        model = Card
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['seller'] = user.shop_owner
        return attrs


class RateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs


class CommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = 'datetime',

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs


class RateGetSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = Rate
        fields = '__all__'


class CommentGetSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    datetime = TimestampField(required=False)

    class Meta:
        model = Comment
        fields = '__all__'


class ShopRateCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopRate
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs


class ShopCommentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShopComment
        exclude = 'datetime',

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs


class ShopRateGetSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()

    class Meta:
        model = ShopRate
        fields = '__all__'


class ShopCommentGetSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer()
    datetime = TimestampField(required=False)

    class Meta:
        model = ShopComment
        fields = '__all__'


class DeliverChoiceGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DelieverChoice
        fields = '__all__'


class PaymentChoiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentChoice
        fields = '__all__'


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ShortShopSerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer()
    products_amount = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    def get_average_rate(self, shop):
        return (
            shop.shop_rate.all().aggregate(Avg('rate')) if shop.shop_rate.all() else 0
        )

    def get_products_amount(self, shop):
        return len(shop.card_creator.all())

    class Meta:
        model = Shop
        exclude = 'schedule', 'description'


class CardGetShortSerializer(serializers.ModelSerializer):
    calc_price = serializers.SerializerMethodField()
    comments_amount = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    seller = ShortShopSerializer()

    def get_preview(self, card):
        request = self.context.get('request')
        if card.preview and getattr(card.preview, 'url'):
            file_url = card.preview.url
            return request.build_absolute_uri(file_url)
        return None

    def get_comments_amount(self, card):
        return card.card_comment.all().annotate(num_comments=Count('comment'))[0].num_comments if card.card_comment.all() else 0

    def get_average_rate(self, card):
        return (
            card.card_rate.all().aggregate(Avg('rate')) if card.card_rate.all() else 0
        )

    def get_calc_price(self, card):
        if card.discount_price != 0:
            return card.discount_price
        return card.price

    class Meta:
        model = Card
        fields = (
            'pk',
            'title',
            'price',
            'discount_price',
            'preview',
            'calc_price',
            'comments_amount',
            'average_rate',
            'seller',
        )


class CardGetSerializer(serializers.ModelSerializer):
    seller = ShortShopSerializer()
    payment_methods = PaymentChoiceGetSerializer(many=True)
    deliver_methods = DeliverChoiceGetSerializer(many=True)
    category = CategoryShortSerializer()
    calc_price = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True)
    comments = serializers.SerializerMethodField()
    comments_amount = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    characteristics = serializers.SerializerMethodField()

    def get_characteristics(self, card):
        return CardCharacteristicGetShortSerizlier(many=True, instance=card.card_characteristic.all()).data

    def get_average_rate(self, card):
        return (
            card.card_rate.all().aggregate(Avg('rate')) if card.card_rate.all() else 0
        )

    def get_rate(self, card):
        return [RateGetSerializer(instance=rate).data for rate in card.card_rate.all()]

    def get_comments(self, card):
        return [CommentGetSerializer(instance=comm, context={'request':  self.context.get('request')}).data for comm in card.card_comment.all().order_by('-datetime')]

    def get_comments_amount(self, card):
        return card.card_comment.all().annotate(num_comments=Count('comment'))[0].num_comments if card.card_comment.all() else 0

    def get_calc_price(self, card):
        if card.discount_price != 0:
            return card.discount_price
        return card.price

    class Meta:
        model = Card
        fields = (
            'pk',
            'title',
            'description',
            'seller',
            'present',
            'discount_price',
            'preview',
            'attachments',
            'category',
            'payment_methods',
            'deliver_methods',
            'calc_price',
            'comments',
            'comments_amount',
            'rate',
            'average_rate',
            'characteristics',
        )


class SellersSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    average_rate = serializers.SerializerMethodField()
    products_amount = serializers.SerializerMethodField()
    shop_logo = serializers.SerializerMethodField()
    shop_title = serializers.SerializerMethodField()
    shop_id = serializers.SerializerMethodField()

    def get_shop_title(self, user: User):
        return user.shop_owner.name

    def get_shop_id(self, user: User):
        return user.shop_owner.pk

    def get_shop_logo(self, user: User):
        request = self.context.get('request')
        if user.shop_owner.logo and getattr(user.shop_owner.logo, 'url'):
            file_url = user.shop_owner.logo.url
            return request.build_absolute_uri(file_url)
        return None

    def get_average_rate(self, user: User):
        return (
            user.shop_owner.average_rate() if user.customer else 0
        )

    def get_products_amount(self, user: User):
        return (
            len(user.shop_owner.card_creator.all()) if user.customer else 0
        )

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'image',
            'fio',
            'customer',
            'verified',
            'top_seller',
            'average_rate',
            'products_amount',
            'shop_logo',
            'shop_title',
            'shop_id',
        )


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'


class ShopGetSerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer()
    schedule = ScheduleSerializer(required=False, many=True)
    comments = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    last_sold_products = serializers.SerializerMethodField()
    top_products = serializers.SerializerMethodField()
    last_orders = serializers.SerializerMethodField()
    comments_amount = serializers.SerializerMethodField()
    products_amount = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    rates = serializers.SerializerMethodField()

    def get_rates(self, shop: Shop):
        ...

    def get_categories(self, shop):
        shop_cards = shop.card_creator.all()
        categories = set([card.category for card in shop_cards])
        return CategoryShortSerializer(instance=categories, many=True, context={'request': self.context.get('request')}).data

    def get_last_orders(self, shop):
        shop_cards = shop.card_creator.all()
        orders = []
        for card in shop_cards:
            for order_item_card in card.order_item.all():
                for order in order_item_card.order_items.all().order_by('-created_at'):
                    orders.append(order)
        orders = set(orders)
        orders = sorted(orders, key=lambda x: x.created_at, reverse=True)[:3]
        return OrderGetSerializer(instance=orders, many=True, context={'request': self.context.get('request')}).data

    def get_last_sold_products(self, shop):
        orders = Order.objects.filter(approved=True).order_by('-pk')
        res_orders = []
        for order in orders:
            for order_item in order.items.filter(item__seller=shop).order_by('-pk').distinct():
                if len(res_orders) < 3:
                    res_orders.append(CardGetShortSerializer(
                        instance=order_item.item, context={'request': self.context.get('request')}).data)
                else:
                    break
            if len(res_orders) >= 3:
                break
        return res_orders

    def get_average_rate(self, shop):
        return (
            shop.shop_rate.all().aggregate(Avg('rate')) if shop.shop_rate.all() else 0
        )

    def get_rate(self, shop):
        return [ShopRateGetSerializer(instance=rate).data for rate in shop.shop_rate.all()]

    def get_comments(self, shop):
        return [ShopCommentGetSerializer(instance=comm).data for comm in shop.shop_comment.all().order_by('-datetime')]

    def get_comments_amount(self, shop):
        return shop.shop_comment.all().annotate(num_comments=Count('comment'))[0].num_comments if shop.shop_comment.all() else 0

    def get_products_amount(self, shop):
        return len(shop.card_creator.all())

    def get_top_products(self, shop):
        products = CardGetShortSerializer(
            instance=shop.card_creator.all(),
            many=True,
            context={'request': self.context.get('request')}
        ).data
        products = sample(products, 5 if len(products) > 5 else len(products)),
        return products[0]

    class Meta:
        model = Shop
        fields = '__all__'


class ShopCreateSerializer(serializers.ModelSerializer):

    schedule = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(), many=True, required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Shop
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['owner'] = user
        return attrs


class ShopUpdateSerializer(serializers.ModelSerializer):

    schedule = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(), many=True, required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    logger = serializers.ImageField(required=False)

    class Meta:
        model = Shop
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['owner'] = user
        return attrs


class OrderItemCreateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemUpdateSerializer(serializers.ModelSerializer):
    item = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(), required=False)
    quantity = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderItemGetShortSerializer(serializers.ModelSerializer):
    item = CardGetShortSerializer()

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderCreateSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all())
    coupon = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(), required=False)
    items = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem.objects.all(), many=True, required=False)

    class Meta:
        model = Order
        exclude = (
            'created_at',
            'being_delivered',
            'received',
            'refund_requested',
            'refund_granted',
            'ordered',
            'approved',
        )

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs


class OrderGetSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all())
    items = OrderItemGetShortSerializer(many=True)
    created_at = TimestampField()
    coupon = CouponSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderGetShortSerializer(serializers.ModelSerializer):
    user = UserShortSerializer()
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all())
    items = OrderItemGetShortSerializer(many=True)
    created_at = TimestampField()
    coupon = CouponSerializer()
    address = AddressSerializer()

    class Meta:
        model = Order
        fields = '__all__'


class OrderUpdateSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(
        queryset=Address.objects.all(), required=False)
    coupon = serializers.PrimaryKeyRelatedField(
        queryset=Coupon.objects.all(), required=False)
    items = serializers.PrimaryKeyRelatedField(
        queryset=OrderItem.objects.all(), many=True, required=False)
    approved = serializers.BooleanField(required=False)
    oredered = serializers.BooleanField(required=False)
    being_delievered = serializers.BooleanField(required=False)
    recieved = serializers.BooleanField(required=False)
    refund_requested = serializers.BooleanField(required=False)
    refund_granted = serializers.BooleanField(required=False)
    fio = serializers.CharField(required=False)
    comment = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)

    class Meta:
        model = Order
        exclude = (
            'created_at',
        )

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['user'] = user
        return attrs
