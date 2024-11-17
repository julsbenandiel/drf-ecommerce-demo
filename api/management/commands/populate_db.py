from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from api.models import User, Product, Order, OrderItem
import random
from decimal import Decimal

class Command(BaseCommand):
  help = 'Creates application data'

  def handle(self, *args, **kwargs):
    user = User.objects.filter(username='julsbenandiel').first()
    if not user:
      user = User.objects.create_superuser(username='admin', password='admin123')

    products = [
      Product(name="Iphone 12 pro max", description=lorem_ipsum.paragraph(), price=Decimal('12.99'), stock=4),
      Product(name="Protein Shake", description=lorem_ipsum.paragraph(), price=Decimal('70.99'), stock=6),
    ]

    Product.objects.bulk_create(products)
    products = Product.objects.all()

    # create some dummy orders tied to the superuser
    for _ in range(3):
        # create an Order with 2 order items
        order = Order.objects.create(user=user)
        for product in random.sample(list(products), 2):
            OrderItem.objects.create(
                order=order, 
                product=product,
                quantity=random.randint(1,3)
            )