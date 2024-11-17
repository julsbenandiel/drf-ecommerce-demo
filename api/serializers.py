from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
  class Meta():
    model = Product
    fields = '__all__'

  def validate_price(self, value):
    if value <= 0:
      raise serializers.ValidationError("Price must be greater than 0")
    return value
  
class OrderItemSerializer(serializers.ModelSerializer):
  product = ProductSerializer()

  class Meta():
    model = OrderItem
    fields = [
      'id',
      'item_subtotal',
      'product',
      'quantity'
    ]
  
class OrderSerializer(serializers.ModelSerializer):
  order_items = OrderItemSerializer(many=True, read_only=True)
  total_price = serializers.SerializerMethodField(method_name='total')

  def total(self, obj):
    order_items = obj.order_items.all()
    return sum(order_item.item_subtotal for order_item in order_items)

  class Meta():
    model = Order
    fields = '__all__'

  