from django.urls import path
from .views import (
    CategoryListAPI,
    DelieveryChoiceListAPI,
    PaymentChoiceListAPI,
    CardGetAPI,
    CardCreateAPI,
    RateCreateAPI,
    CommentCreateAPI,
)

urlpatterns = [
    path('categories-list/', CategoryListAPI.as_view(), name=''),
    path('delivery-list/', DelieveryChoiceListAPI.as_view(), name=''),
    path('payment-list/', PaymentChoiceListAPI.as_view(), name=''),
    path('card-get/<int:pk>', CardGetAPI.as_view(), name=''),
    path('card-create/', CardCreateAPI.as_view(), name=''),
    path('rate-create/', RateCreateAPI.as_view(), name=''),
    path('comment-create/', CommentCreateAPI.as_view(), name=''),
]
