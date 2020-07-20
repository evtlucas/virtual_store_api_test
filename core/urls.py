from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from core import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='products_details'),
    path('people/', views.PersonList.as_view(), name='people'),
    path('people/<int:pk>/', views.PersonDetail.as_view(), name='person'),
    path('companies/', views.CompanyList.as_view(), name='companies'),
    path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company'),
    path('customers/', views.CustomerList.as_view(), name='customers'),
    path('orders/', views.OrderList.as_view(), name='orders'),
    path('orders/<int:pk>/', views.OrderDetail.as_view(), name='order'),
    path('orders/<int:order_pk>/items/', views.OrderItemList.as_view(), name='order_items'),
    path('orders/<int:order_pk>/items/<int:pk>/', views.OrderItemDetail.as_view(), name='order_item_detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
