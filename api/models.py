from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
  pass

class Product(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  name = models.CharField(max_length=200)
  description = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now_add=True)

  @property
  def in_stock(self):
    return self.stock > 0

  def __str__(self) -> str:
    return f"{self.name} - {self.description}"
  
class Order(models.Model):
  class StatusOptions(models.TextChoices):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'

  order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(
    max_length=10,
    choices=StatusOptions.choices,
    default=StatusOptions.PENDING
  )

  products = models.ManyToManyField(Product, through='OrderItem')

  def __str__(self) -> str:
    return f"Order {self.order_id} by {self.user.username}"
  
class OrderItem(models.Model):
  order = models.ForeignKey(
    Order,
    on_delete=models.CASCADE,
    related_name='order_items'
  )
  product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
  quantity = models.PositiveIntegerField()

  @property
  def item_subtotal(self) -> float:
    return self.quantity * self.product.price
  
  def __str__(self) -> str:
    return f"{self.quantity} x {self.product.name} in Order {self.order.order_id}"