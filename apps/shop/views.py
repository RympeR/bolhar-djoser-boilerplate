from rest_framework import generics, permissions
from rest_framework.response import Response
from apps.users.models import User
from .models import (
    Category,
    PaymentChoice,
    DelieverChoice,
    Comment,
    Rate,
    Card,
)
from .serializers import (
    CategoryGetSerializer,
    CardGetSerializer,
    RateCreateSerializer,
    CommentCreateSerializer,
    DeliverChoiceGetSerializer,
    PaymentChoiceGetSerializer,
    CardCreateSerializer,
    SellersSerializer,
)


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
        ).order_by('-rank')
        sellers.append(sold_user)
        all_sellers = User.objects.filter(
            top_seller=False,
            customer=True
        )
        sellers.append(all_sellers)
        return Response([self.get_serializer(instance=seller) for seller in all_sellers])
