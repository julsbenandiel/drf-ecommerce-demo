from django.core.management.base import BaseCommand
from api.models import User

class Command(BaseCommand):
  help = 'Creates testing users'

  def handle(self, *args, **kwargs):
    User.objects.create_superuser(username='julsbenandiel', password='admin123')
    
  