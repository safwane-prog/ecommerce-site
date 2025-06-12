from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('contact/', views.contact, name='contact'),
    path('shop/', views.shop, name='shop'),
    path('products/', views.ShopPageView.as_view(), name='shop-by-category'),
]