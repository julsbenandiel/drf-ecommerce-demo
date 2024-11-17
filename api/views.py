from http import HTTPStatus
from api.serializers import ProductSerializer, OrderSerializer
from api.models import Product, Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import json

@api_view(['GET'])
def product_list(request):
  products = Product.objects.all()
  serializer = ProductSerializer(products, many=True)

  return Response(serializer.data, HTTPStatus.OK)

@api_view(['GET'])
def get_product_by_id(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  serializer = ProductSerializer(product)
  
  return Response(serializer.data, HTTPStatus.OK)

@api_view(['GET'])
def get_orders(request):
  orders = Order.objects.all()
  serializer = OrderSerializer(orders, many=True)
  
  return Response(serializer.data, HTTPStatus.OK)

@api_view(['PATCH', 'PUT'])
def update_order_status(request, order_id):
  order = get_object_or_404(Order, pk=order_id)
  data = json.loads(request.body)
  status = data.get('status')

  if not status:
    return Response({ 'message': 'status is missing'}, HTTPStatus.BAD_REQUEST)
  
  if status not in Order.StatusOptions.values:
    return Response({ 'message': 'invalid order status' }, HTTPStatus.BAD_REQUEST)
  
  order.status = status
  order.save()
  
  return Response({
    'message': f'order {order.order_id} status has been updated to {status}'
  }, HTTPStatus.OK)
