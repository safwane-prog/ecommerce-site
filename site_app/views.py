from django.shortcuts import render
# Create your views here.

def home(request):
    return render(request,'home.html')


def product_detail_view(request, pk):
    return render(request, 'product_detail.html')


def contact(request):
    return render(request,'contact.html')


def shop(request):
    return render(request,'shop.html')


from django.views import View
from django.shortcuts import render

class ShopPageView(View):
    def get(self, request):
        return render(request, 'shop_by_category.html')














