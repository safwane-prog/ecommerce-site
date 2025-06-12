from django.db import models

class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=500)
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    colors = models.ManyToManyField(Color, blank=True, related_name='products')
    sizes = models.ManyToManyField(Size, blank=True, related_name='products')
    # Added 10 image fields
    image_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_2 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_2 = models.TextField(null=True, blank=True)
    image_3 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_3 = models.TextField(null=True, blank=True)
    image_4 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_4 = models.TextField(null=True, blank=True)
    image_5 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_5 = models.TextField(null=True, blank=True)
    image_6 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_6 = models.TextField(null=True, blank=True)
    image_7 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_7 = models.TextField(null=True, blank=True)
    image_8 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_8 = models.TextField(null=True, blank=True)
    image_9 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_9 = models.TextField(null=True, blank=True)
    image_10 = models.ImageField(upload_to='products/', null=True, blank=True)
    description_10 = models.TextField(null=True, blank=True)
    # Added 2 video fields
    video_1 = models.FileField(upload_to='products/videos/', null=True, blank=True)
    description_11 = models.TextField(null=True, blank=True)
    video_2 = models.FileField(upload_to='products/videos/', null=True, blank=True)
    description_12 = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.product.name} ({self.quantity})"



class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.subject[:30]}"



from django.db import models

class AdminContactInfo(models.Model):
    phone_number = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    address = models.TextField(verbose_name="العنوان")
    working_hours = models.CharField(max_length=100, verbose_name="ساعات العمل")
    map_link = models.URLField(blank=True, null=True, verbose_name="رابط الخريطة")
    whatsapp_link = models.URLField(blank=True, null=True, verbose_name="رابط واتساب")
    instagram_link = models.URLField(blank=True, null=True, verbose_name="رابط إنستغرام")
    facebook_link = models.URLField(blank=True, null=True, verbose_name="رابط فيسبوك")
    youtube_link = models.URLField(blank=True, null=True, verbose_name="رابط يوتيوب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخر تحديث")

    class Meta:
        verbose_name = "بيانات التواصل"
        verbose_name_plural = "بيانات التواصل"

    def __str__(self):
        return f"معلومات التواصل ({self.email})"




class StoreSettings(models.Model):
    store_name = models.CharField(max_length=255)
    store_logo = models.ImageField(upload_to='store_logos/')

    def __str__(self):
        return self.store_name
    


class AdminProfile(models.Model):
    admin_name = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='admin_profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin_name
