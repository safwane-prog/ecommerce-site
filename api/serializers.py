from rest_framework import serializers, viewsets
from .models import Product, Color, Size, Category,ProductOrder,StoreSettings,AdminProfile

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'name']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


from rest_framework import serializers
from .models import Product, Color, Size, Category

class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.PrimaryKeyRelatedField(
        queryset=Color.objects.all(),
        many=True,
        required=True
    )
    sizes = serializers.PrimaryKeyRelatedField(
        queryset=Size.objects.all(),
        many=True,
        required=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )

    # إضافة حقول لعرض أسماء الألوان والمقاسات
    colors_names = serializers.SerializerMethodField()
    sizes_names = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'  # يمكنك تحديد الحقول يدويًا لو تريد
        # مثلاً: fields = ['id', 'name', 'colors', 'colors_names', 'sizes', 'sizes_names', 'category', 'category_name', ...]

    def get_colors_names(self, obj):
        return [color.name for color in obj.colors.all()]  # استبدل "name" بحقل الاسم الفعلي في موديل Color

    def get_sizes_names(self, obj):
        return [size.name for size in obj.sizes.all()]  # استبدل "name" بحقل الاسم الفعلي في موديل Size

    def get_category_name(self, obj):
        return obj.category.name  # استبدل "name" بحقل الاسم الفعلي في موديل Category



# serializers.py
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = '__all__'
# products/serializers.py


class BestSellingProductSerializer(serializers.ModelSerializer):
    total_sales = serializers.IntegerField()

    class Meta:
        model = Product
        fields = '__all__'

        
from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'full_name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']
from rest_framework import serializers
from .models import AdminContactInfo

class AdminContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminContactInfo
        fields = '__all__'


from rest_framework import serializers
from .models import ProductOrder, Product

from rest_framework import serializers
from .models import ProductOrder, Product

class Productserializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    product_details = Productserializers(source='product', read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductOrder
        fields = ['id', 'product', 'product_details', 'full_name', 'phone', 'address', 'color', 'size', 'quantity', 'created_at', 'is_paid']
        read_only_fields = ['id', 'created_at', 'full_name', 'phone', 'address', 'color', 'size', 'quantity', 'product']


class ContactSerializer_2(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'



class StoreSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreSettings
        fields = '__all__'




class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminProfile
        fields = [
            'id',
            'admin_name',
            'profile_image',
            'phone_number',
            'address',
            'position',
            'bio',
            'created_at',
            'updated_at'
        ]
