from django.shortcuts import render, redirect,get_object_or_404
from api.models import Product



def dashboard(request):
    return render(request,'dashboard.html')

def views_product(request):
    return render (request,'viiew_products.html')
# 
def add_product_view(request):
    return render(request, 'add_product.html')

def orders(request):
    return render(request,'orders.html')

def edit_product(request,id):
    product = get_object_or_404(Product,id=id)
    return render(request,'edit_product.html',{'product':product})

def massage(request):
    return render (request,'massage.html')

def settings(request):
    return render (request,'settings.html')
