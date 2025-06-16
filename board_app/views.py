from django.shortcuts import render, redirect,get_object_or_404
from api.models import Product
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    return render(request,'dashboard.html')
@staff_member_required
def views_product(request):
    return render (request,'viiew_products.html')
@staff_member_required
def add_product_view(request):
    return render(request, 'add_product.html')
@staff_member_required
def orders(request):
    return render(request,'orders.html')
@staff_member_required
def edit_product(request,id):
    product = get_object_or_404(Product,id=id)
    return render(request,'edit_product.html',{'product':product})
@staff_member_required
def massage(request):
    return render (request,'massage.html')
@staff_member_required
def settings(request):
    return render (request,'settings.html')


