from rest_framework import views, permissions, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from products.models import Product

class CartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user)
        serializer = CartItemSerializer(items, many=True)
        total = sum(item.subtotal for item in items)
        return Response({
            'items': serializer.data,
            'total': total
        })

class AddToCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product')
        quantity = int(request.data.get('quantity', 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': quantity}
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

class UpdateCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))

        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        if quantity <= 0:
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        item.quantity = quantity
        item.save()
        return Response(CartItemSerializer(item).data)

class RemoveFromCartView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, user=request.user)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)
