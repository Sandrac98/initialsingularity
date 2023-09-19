from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_products, name='products'),
    path('products/product_details/<int:product_id>/', views.product_details, name='product_details')  # noqa
]
