from apps.users.serializers import UserShortSerializer
from rest_framework.views import APIView
from apps.utils.customClasses import (
    SellersPagination,
    CardFilter,
    SellersFilter,
)
from apps.users.models import User
from .models import (
    Category,
    MainSlider,
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
    MainSlider,
    ProductBrand,
    ProductCountry,
)
from .serializers import (
    CardGetShortSerializer,
    CategoryGetSerializer,
    CardGetSerializer,
    CategoryShortSerializer,
    RateCreateSerializer,
    CommentCreateSerializer,
    DeliverChoiceGetSerializer,
    PaymentChoiceGetSerializer,
    CardCreateSerializer,
    SellersSerializer,
    ShopRateCreateSerializer,
    ShopCommentCreateSerializer,
    CouponSerializer,
    AddressSerializer,
    ScheduleSerializer,
    ShopGetSerializer,
    ShopCreateSerializer,
    ShopUpdateSerializer,
    OrderItemCreateSerializer,
    OrderItemUpdateSerializer,
    OrderItemGetShortSerializer,
    OrderCreateSerializer,
    OrderGetSerializer,
    OrderUpdateSerializer,
    MainSliderSerializer,
    ProductBrandGetSerializer,
    ProductCountryGetSerializer,
)
import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from random import sample


class CardFilteredAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = Card.objects.all()
    filterset_class = CardFilter
    serializer_class = CardGetShortSerializer


class CardLatestAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = Card.objects.all().order_by('-pk')[:10]
    serializer_class = CardGetShortSerializer


class CategoryListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = Category.objects.all()
    serializer_class = CategoryGetSerializer

class BrandsListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = ProductBrand.objects.all()
    serializer_class = ProductBrandGetSerializer

class CountryListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = ProductCountry.objects.all()
    serializer_class = ProductCountryGetSerializer


class DelieveryChoiceListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = DelieverChoice.objects.all()
    serializer_class = DeliverChoiceGetSerializer


class PaymentChoiceListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = PaymentChoice.objects.all()
    serializer_class = PaymentChoiceGetSerializer


class CardGetAPI(generics.RetrieveAPIView):
    permissions = permissions.AllowAny,
    queryset = Card.objects.all()
    serializer_class = CardGetSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CardCreateAPI(generics.CreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class RateCreateAPI(generics.CreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentCreateAPI(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class SellersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SellersSerializer
    paginate_class = SellersPagination
    filterset_class = SellersFilter

    def get_queryset(self):
        all_sellers = User.objects.filter(
            customer=True
        ).order_by('top_seller', '-user_rate_shop')
        return all_sellers.distinct()


class ShopCommentCreateAPI(generics.CreateAPIView):
    queryset = ShopComment.objects.all()
    serializer_class = ShopCommentCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ShopRateCreateAPI(generics.CreateAPIView):
    queryset = ShopRate.objects.all()
    serializer_class = ShopRateCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ShopCreateAPI(generics.CreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ShopDeleteAPI(generics.DestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopCreateSerializer


class ShopGetAPI(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopGetSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ShopPartialUpdateAPI(GenericAPIView, UpdateModelMixin):
    queryset = ShopRate.objects.all()
    serializer_class = ShopUpdateSerializer

    def get_object(self):
        user = self.request.user
        return user.shop_owner

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class CouponCreateAPI(generics.CreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class AddressCreateAPI(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ScheduleCreateAPI(generics.CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class OrderItemCreateAPI(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class OrderItemGetAPI(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemGetShortSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class OrderItemDeleteAPI(generics.DestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemGetShortSerializer


class OrderItemUpdateAPI(GenericAPIView, UpdateModelMixin):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OrderCreateAPI(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class OrderGetAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer

    def get_object(self):
        user = self.request.user
        return user.order_user.filter(approved=False).first()

    def get_serializer_context(self):
        return {'request': self.request}

class SingleOrderGetAPI(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class OrderUpdateAPI(GenericAPIView, UpdateModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer

    def get_object(self):
        user = self.request.user
        return user.order_user.filter(approved=False)

    def get_serializer_context(self):
        return {'request': self.request}

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class ShopOrderGetAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        shop = user.shop_owner
        shop_cards = shop.card_creator.all()
        orders = []
        for card in shop_cards:
            for order_item_card in card.order_item.all():
                for order in order_item_card.order_items.all().order_by('-created_at'):
                    orders.append(order)
        orders = set(orders)
        orders = sorted(orders, key=lambda x: x.created_at, reverse=True)
        return orders

class UserOrderGetAPI(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        orders = user.order_user.all()
        return orders

class UserFavouritesAPI(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardGetShortSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        user = self.request.user
        favourites = user.user_favourite.all()
        return favourites


class MainSliderListAPI(generics.ListAPIView):
    queryset = MainSlider.objects.all()
    serializer_class = MainSliderSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class MainPageAPI(APIView):

    def get(self, request):
        result = {}
        sliders = MainSlider.objects.all()
        slider = MainSliderSerializer(
            instance=sliders,
            many=True,
            context={'request': request}
        ).data
        slider = sample(slider, 5 if len(slider) > 5 else len(slider))
        result['slider'] = slider
        categories = Category.objects.all()
        categories = CategoryShortSerializer(
            instance=categories,
            many=True,
            context={'request': request}
        ).data
        categories = sample(categories, 5 if len(
            categories) > 5 else len(categories))
        result['categories'] = categories
        sellers = User.objects.filter(top_seller=True)[:3]
        sellers = SellersSerializer(
            instance=sellers,
            many=True,
            context={'request': request}
        ).data
        result['sellers'] = sellers
        products = Card.objects.all().order_by('-pk')[:100]
        products = CardGetShortSerializer(
            instance=products, context={'request': request}, many=True
        ).data
        slider = sample(products, 10 if len(products) > 10 else len(products))
        result['products'] = products
        user = request.user
        if user.shop_owner:
            result['has_shop'] = True
            result['shop_id'] = user.shop_owner.pk
        else:
            result['has_shop'] = False
        result['user'] = UserShortSerializer(instance=user, context={'request': request}).data
        return Response(result)
