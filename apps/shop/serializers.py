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
)


class CategoryGetSerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Category.objects.all(),)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CardCreateSerializer(serializers.ModelSerializer):

    seller = serializers.PrimaryKeyRelatedField(
        required=False, queryset=User.objects.all())
    discount_price = serializers.FloatField(required=False)

    class Meta:
        model = Card
        fields = '__all__'

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        attrs['seller'] = user
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


class CardGetShortSerializer(serializers.ModelSerializer):
    calc_price = serializers.SerializerMethodField()
    comments_amount = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    def get_comments_amount(self, card):
        return card.card_comment.all().annotate(num_comments=Count('comment')).num_comments if card.card_comment.all() else 0

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
            'title',
            'price',
            'discount_price',
            'preview',
            'calc_price',
            'comments_amount',
            'average_rate',
        )


class CardGetSerializer(serializers.ModelSerializer):
    seller = ShortUserSerializer()
    payment_methods = PaymentChoiceGetSerializer(many=True)
    deliver_methods = DeliverChoiceGetSerializer(many=True)
    category = CategoryShortSerializer()
    calc_price = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True)
    comments = serializers.SerializerMethodField()
    comments_amount = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    def get_average_rate(self, card):
        return (
            card.card_rate.all().aggregate(Avg('rate')) if card.card_rate.all() else 0
        )

    def get_rate(self, card):
        return [RateGetSerializer(instance=rate).data for rate in card.card_rate.all()]

    def get_comments(self, card):
        return [CommentGetSerializer(instance=comm).data for comm in card.card_comment.all().order_by('-datetime')]

    def get_comments_amount(self, card):
        return card.card_comment.all().annotate(num_comments=Count('comment')).num_comments if card.card_comment.all() else 0

    def get_calc_price(self, card):
        if card.discount_price != 0:
            return card.discount_price
        return card.price

    class Meta:
        model = Card
        fields = (
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
            'characteristics',
            'calc_price',
            'comments',
            'comments_amount',
            'rate',
            'average_rate',
        )


class SellersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'image',
            'fio',
            'verified'
        )


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'


class ShopGetSerializer(serializers.ModelSerializer):
    owner = ShortUserSerializer()
    schedule = ScheduleSerializer()
    comments = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()
    last_sold_products = serializers.SerializerMethodField()

    def last_sold_products(self, shop):
        # CardGetShortSerializer
        ...

    def get_average_rate(self, shop):
        return (
            shop.shop_rate.all().aggregate(Avg('rate')) if shop.shop_rate.all() else 0
        )

    def get_rate(self, shop):
        return [ShopRateGetSerializer(instance=rate).data for rate in shop.shop_rate.all()]

    def get_comments(self, shop):
        return [ShopCommentGetSerializer(instance=comm).data for comm in shop.card_comment.all().order_by('-datetime')]

    class Meta:
        model = Shop
        fields = '__all__'


class ShopCreateSerializer(serializers.ModelSerializer):

    schedule = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all(), many=True, required=False)

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
    create_at = TimestampField()
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
