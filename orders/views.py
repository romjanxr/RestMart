from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from orders.serializers import EmptySerializer, OrderSerializer, CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, CreateOrderSerializer, UpdateOrderSerializer
from orders.models import Cart, CartItem, Order, OrderItem
from orders.services import OrderService
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

# Create your views here.
class CartViewset(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user)

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk')).select_related('product')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        return {'cart_id': self.kwargs.get('cart_pk')}

            
class OrderViewset(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']
    serializer_class = OrderSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def cancel(self, request, *args, **kwargs):
        order = self.get_object()
        OrderService.cancel_order(order, request.user)
        return Response({'status': 'Order cancelled'}, status=status.HTTP_201_CREATED)
        

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = UpdateOrderSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(OrderSerializer(order).data)

    def get_permissions(self):
        if self.action in ['update_status', 'destroy' ]:
            return [IsAdminUser()]
        return[IsAuthenticated()]
        

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        user = self.request.user
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if user.is_staff:
            return Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=user)

    def get_serializer_class(self):
        if self.action == 'cancel':
            return EmptySerializer
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
