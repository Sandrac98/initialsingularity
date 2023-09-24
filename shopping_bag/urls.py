from django.urls import path
from . import views

urlpatterns = [
    path('shopping_bag/', views.view_shopping_bag, name='view_shopping_bag'),
    path('add/<item_id>/', views.add_to_shopping_bag, name='add_to_shopping_bag'),  # noqa
    path('update/<item_id>/', views.update_shopping_bag, name='update_shopping_bag'),  # noqa
    path('remove/<item_id>/', views.remove_from_shopping_bag, name='remove_from_shopping_bag'),  # noqa
]
