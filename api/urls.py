from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from django.shortcuts import render

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'colors', ColorViewSet)
router.register(r'sizes', SizeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'admin-order', ProductOrderViewSet, basename='orders')
router.register(r'contact-view', ContactViewSet, basename='contact-view')
router.register(r'admin-profile', AdminProfileViewSet, basename='AdminProfileViewSet-view')

urlpatterns = [
    path('', include(router.urls)),
    path('orders/', OrderCreateAPIView.as_view(), name='orders_2'),
    path('orders-free/', ProductOrderAPIView.as_view(), name='product-order'),
    path('best-selling/', BestSellingProductsAPIView.as_view(), name='best-selling-products'),
    path('contact/', ContactCreateAPIView.as_view(), name='contact-api'),
    path('contact-info/', AdminContactInfoView.as_view(), name='contact-info'),
    path('dashboard-full-stats/', AdvancedDashboardStatsAPIView.as_view(), name='dashboard-full-stats'),
    path('store-settings/', StoreSettingsRetrieveUpdateView.as_view(), name='store-settings'),
    path('notifications/', NotificationListView.as_view()),
    path('notifications/delete-all/', NotificationDeleteAllView.as_view()),
]