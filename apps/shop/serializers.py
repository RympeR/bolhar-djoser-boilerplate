from rest_framework import serializers
from django.db.models import Avg
from apps.users.serializers import (
    ShortUserSerializer
)
from apps.users.models import (
    User
)
from apps.chat.serializers import AttachmentSerializer
from .models import (
    Category,
    PaymentChoice,
    DelieverChoice,
    Comment,
    Rate,
    Card,
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

    class Meta:
        model = Comment
        fields = '__all__'


class DeliverChoiceGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = DelieverChoice
        fields = '__all__'


class PaymentChoiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentChoice
        fields = '__all__'


class CardGetSerializer(serializers.ModelSerializer):
    seller = ShortUserSerializer()
    payment_methods = PaymentChoiceGetSerializer(many=True)
    deliver_methods = DeliverChoiceGetSerializer(many=True)
    category = CategoryShortSerializer()
    calc_price = serializers.SerializerMethodField()
    attachments = AttachmentSerializer(many=True)
    comments = serializers.SerializerMethodField()
    rate = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField()

    def get_average_rate(self, card):
        return (
            card.card_rate.all().aggregate(Avg('rate')) if card.card_rate.all() else 0
        )

    def get_rate(self, card):
        return [RateGetSerializer(instance=rate) for rate in card.card_rate.all()]

    def get_comments(self, card):
        return [CommentGetSerializer(instance=comm) for comm in card.card_comment.all().order_by('-datetime')]

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
            'rate',
            'average_rate',
        )
