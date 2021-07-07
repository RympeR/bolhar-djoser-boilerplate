from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from django_filters import rest_framework as filters
from django.db.models import Q
from apps.users.models import User
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
from .serializers import (
    CategoryGetSerializer,
    CardGetSerializer,
    RateCreateSerializer,
    CommentCreateSerializer,
    DeliverChoiceGetSerializer,
    PaymentChoiceGetSerializer,
    CardCreateSerializer,
    CategoryShortSerializer,
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
)


def filter_related_objects(queryset, name, value, model, serializer, related_category):
    lookup = '__'.join([name, 'in'])
    if value:
        subjects = model.objects.filter(pk__in=[obj.pk for obj in value])
        look_related = '__'.join([related_category, 'gte'])
        result = []
        for subj in subjects:
            hole_tree = model.objects.filter(
                Q(tree_id=subj.tree_id) &
                Q(**{look_related: getattr(subj, related_category)}) &
                Q(display=True)
            )
            values = [serializer(
                instance=subject).data['id'] for subject in hole_tree]
            result.append(values)
        values = result
    else:
        subjects = model.objects.filter(display=True)
        values = [serializer(
            instance=subject).data['id'] for subject in subjects]
    res = []
    for value in values:
        if isinstance(value, list):
            res.extend(value)
        else:
            res.append(value)

    return queryset.filter(**{lookup: res}).distinct()


class CardFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    price = filters.NumberFilter(lookup_expr='lte')
    category = filters.ModelMultipleChoiceFilter(
        lookup_expr='in',
        queryset=Category.objects.all(),
        field_name='category',
        method='filter_category'
    )

    def filter_category(self, queryset, name, value):
        return filter_related_objects(queryset, name, value, Category, CategoryShortSerializer, 'Подкатегория категории')

    class Meta:
        model = Card
        fields = (
            'title',
            'seller',
            'price',
            'category',
            'payment_methods',
            'deliver_methods',
            'product_brand',
            'product_country',
        )


class CardFilteredAPI(generics.ListAPIView):
    queryset = Card.objects.all()
    filterset_class = CardFilter
    serializer_class = CardGetSerializer


class CategoryListAPI(generics.ListAPIView):
    permissions = permissions.AllowAny,
    queryset = Category.objects.all()
    serializer_class = CategoryGetSerializer


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

    def list(self, request):
        sellers = []
        sold_user = User.objects.filter(
            top_seller=True,
        ).order_by('-shop_owner__average_rate')
        sellers.append(sold_user)
        all_sellers = User.objects.filter(
            top_seller=False,
            customer=True
        )
        sellers.append(all_sellers)
        return Response([self.get_serializer(instance=seller) for seller in all_sellers])


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
        return user.order_user.filter(approved=False)
    
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
