from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include

from core import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='products'),
    path('products/<int:pk>/', views.ProductDetail.as_view(), name='products_details')
]

urlpatterns = format_suffix_patterns(urlpatterns)
