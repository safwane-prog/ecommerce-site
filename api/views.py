from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import *
from .serializers import *
from rest_framework import generics

@method_decorator(csrf_exempt, name='dispatch')
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category_id')
        print("📌 category_id:", category_id)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset

@method_decorator(csrf_exempt, name='dispatch')
class ColorViewSet(viewsets.ModelViewSet):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class SizeViewSet(viewsets.ModelViewSet):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class OrderCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


from rest_framework.views import APIView
from django.db.models import Count
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import ProductOrder
from .serializers import ProductOrderSerializer
@method_decorator(csrf_exempt, name='dispatch')
class ProductOrderAPIView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    permission_classes = [AllowAny]

class BestSellingProductsAPIView(APIView):
    def get(self, request):
        best_selling_products = Product.objects.annotate(
            total_sales=Count('productorder')
        ).order_by('-total_sales')[:4]

        serializer = BestSellingProductSerializer(best_selling_products, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class ContactCreateAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'تم إرسال رسالتك بنجاح!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class AdminContactInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        info, created = AdminContactInfo.objects.get_or_create(id=1)
        serializer = AdminContactInfoSerializer(info)
        return Response(serializer.data)

    def patch(self, request):
        info, created = AdminContactInfo.objects.get_or_create(id=1)
        serializer = AdminContactInfoSerializer(info, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.authentication import SessionAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # ببساطة نتجاهل CSRF بالكامل

# ثم داخل ViewSet:
class ProductOrderViewSet(viewsets.ModelViewSet):
    queryset = ProductOrder.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = [AllowAny]

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        is_paid = request.data.get('is_paid', None)
        if is_paid is None:
            return Response({"error": "يجب إرسال الحقل is_paid للتعديل."}, status=status.HTTP_400_BAD_REQUEST)

        instance.is_paid = is_paid
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Sum, F

class AdvancedDashboardStatsAPIView(APIView):
    def get(self, request):
        now = timezone.now()

        total_products = Product.objects.count()
        total_categories = Category.objects.count()
        total_orders = ProductOrder.objects.count()

        total_revenue = ProductOrder.objects.filter(is_paid=True).aggregate(
            revenue=Sum(F('product__price') * F('quantity'))
        )['revenue'] or 0

        avg_order_value = (total_revenue / total_orders) if total_orders > 0 else 0
        conversion_rate = 5.2

        last_7_days = now - timedelta(days=7)
        last_30_days = now - timedelta(days=30)
        previous_7_days = now - timedelta(days=14)
        previous_30_days = now - timedelta(days=60)

        orders_7 = ProductOrder.objects.filter(created_at__gte=last_7_days)
        orders_30 = ProductOrder.objects.filter(created_at__gte=last_30_days)

        orders_7_count = orders_7.count()
        orders_30_count = orders_30.count()

        revenue_7 = orders_7.filter(is_paid=True).aggregate(
            revenue=Sum(F('product__price') * F('quantity'))
        )['revenue'] or 0

        revenue_30 = orders_30.filter(is_paid=True).aggregate(
            revenue=Sum(F('product__price') * F('quantity'))
        )['revenue'] or 0

        previous_orders_7_count = ProductOrder.objects.filter(created_at__gte=previous_7_days, created_at__lt=last_7_days).count()
        previous_orders_30_count = ProductOrder.objects.filter(created_at__gte=previous_30_days, created_at__lt=last_30_days).count()

        previous_revenue_7 = ProductOrder.objects.filter(
            created_at__gte=previous_7_days,
            created_at__lt=last_7_days,
            is_paid=True
        ).aggregate(revenue=Sum(F('product__price') * F('quantity')))['revenue'] or 0

        previous_revenue_30 = ProductOrder.objects.filter(
            created_at__gte=previous_30_days,
            created_at__lt=last_30_days,
            is_paid=True
        ).aggregate(revenue=Sum(F('product__price') * F('quantity')))['revenue'] or 0

        order_growth_7 = self.calculate_growth(orders_7_count, previous_orders_7_count)
        order_growth_30 = self.calculate_growth(orders_30_count, previous_orders_30_count)
        revenue_growth_7 = self.calculate_growth(revenue_7, previous_revenue_7)
        revenue_growth_30 = self.calculate_growth(revenue_30, previous_revenue_30)

        category_stats = []
        total_orders_for_percentage = ProductOrder.objects.count() or 1
        for category in Category.objects.all():
            category_orders = ProductOrder.objects.filter(product__category=category)
            revenue = category_orders.filter(is_paid=True).aggregate(
                revenue=Sum(F('product__price') * F('quantity'))
            )['revenue'] or 0

            category_stats.append({
                "category_id": category.id,
                "category_name": category.name,
                "product_count": Product.objects.filter(category=category).count(),
                "order_count": category_orders.count(),
                "revenue": float(revenue),
                "percentage_of_total": round((category_orders.count() / total_orders_for_percentage) * 100, 2)
            })

        top_products_qs = ProductOrder.objects.values(
            'product_id', 'product__name'
        ).annotate(
            order_count=Count('id'),
            revenue=Sum(F('product__price') * F('quantity'))
        ).order_by('-order_count')[:5]

        top_products = [
            {
                "product_id": p['product_id'],
                "product_name": p['product__name'],
                "order_count": p['order_count'],
                "revenue": float(p['revenue'])
            } for p in top_products_qs
        ]

        paid_orders = ProductOrder.objects.filter(is_paid=True).count()
        unpaid_orders = ProductOrder.objects.filter(is_paid=False).count()
        paid_percentage = (paid_orders / total_orders * 100) if total_orders else 0

        size_distribution = []
        for size in Size.objects.all():
            size_orders = ProductOrder.objects.filter(size=size).count()
            size_distribution.append({
                "size_id": size.id,
                "size_name": size.name,
                "order_count": size_orders,
                "percentage": round((size_orders / total_orders) * 100, 2) if total_orders else 0
            })

        color_distribution = []
        for color in Color.objects.all():
            color_orders = ProductOrder.objects.filter(color=color).count()
            color_distribution.append({
                "color_id": color.id,
                "color_name": color.name,
                "order_count": color_orders,
                "percentage": round((color_orders / total_orders) * 100, 2) if total_orders else 0
            })

        data = {
            "status": "success",
            "data": {
                "general_stats": {
                    "total_products": total_products,
                    "total_categories": total_categories,
                    "total_orders": total_orders,
                    "total_revenue": float(total_revenue),
                    "avg_order_value": round(avg_order_value, 2),
                    "conversion_rate": conversion_rate
                },
                "time_based_stats": {
                    "last_7_days": {
                        "new_orders": orders_7_count,
                        "revenue": float(revenue_7),
                        "new_products": Product.objects.filter().count(),
                        "order_growth": round(order_growth_7, 2),
                        "revenue_growth": round(revenue_growth_7, 2)
                    },
                    "last_30_days": {
                        "new_orders": orders_30_count,
                        "revenue": float(revenue_30),
                        "new_products": Product.objects.filter().count(),
                        "order_growth": round(order_growth_30, 2),
                        "revenue_growth": round(revenue_growth_30, 2)
                    }
                },
                "category_stats": category_stats,
                "top_products": top_products,
                "order_status_stats": {
                    "paid_orders": paid_orders,
                    "unpaid_orders": unpaid_orders,
                    "paid_percentage": round(paid_percentage, 2)
                },
                "size_distribution": size_distribution,
                "color_distribution": color_distribution
            },
            "last_updated": now.isoformat()
        }

        return Response(data)

    def calculate_growth(self, current, previous):
        if previous == 0:
            return 100 if current > 0 else 0
        return ((current - previous) / previous) * 100

@method_decorator(csrf_exempt, name='dispatch')
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer_2
    permission_classes = [AllowAny]

@method_decorator(csrf_exempt, name='dispatch')
class StoreSettingsRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = StoreSettings.objects.all()
    serializer_class = StoreSettingsSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        obj, created = StoreSettings.objects.get_or_create(id=1, defaults={'store_name': 'Default Store'})
        return obj

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class AdminProfileViewSet(viewsets.ModelViewSet):
    queryset = AdminProfile.objects.all()
    serializer_class = AdminProfileSerializer
    permission_classes = [AllowAny]


from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer



from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

@method_decorator(csrf_exempt, name='dispatch')
class NotificationDeleteAllView(APIView):
    authentication_classes = []
    permission_classes = []
    def delete(self, request, *args, **kwargs):
        Notification.objects.all().delete()
        return Response({"message": "تم حذف جميع الإشعارات."}, status=204)
