from django.urls import path
from . import views
urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('add/',views.add_product_view,name='add_product'),
    path('products/',views.views_product,name='views_product'),
    path('orders/',views.orders,name='orders'),
    path('massage/',views.massage,name='massage'),
    path('settings/',views.settings,name='settings'),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
]