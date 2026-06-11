from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from cart.models import CartItem
from products.serializers import ProductSerializer

class CreateOrderView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.subtotal for item in cart_items)
        
        # Snapshot products
        products_snapshot = []
        for item in cart_items:
            product_data = ProductSerializer(item.product).data
            products_snapshot.append({
                'product': product_data,
                'quantity': item.quantity,
                'subtotal': float(item.subtotal)
            })

        order = Order.objects.create(
            user=user,
            total_price=total_price,
            products=products_snapshot
        )

        # Clear cart
        cart_items.delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
