from django.urls import path
from . import views

urlpatterns = [
  path('products/', views.product_list),
  path('products/<uuid:product_id>/', views.get_product_by_id),

  path('orders/', views.get_orders),
  path('orders/<uuid:order_id>/update-status/', views.update_order_status)
]
