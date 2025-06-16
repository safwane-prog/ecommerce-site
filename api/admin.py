from django.contrib import admin
from .models import *

# لعرض الصور والفيديوهات داخل صفحة المنتج
admin.site.register(Product)
admin.site.register(Color)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(ProductOrder)
admin.site.register(AdminContactInfo)
admin.site.register(Contact)
admin.site.register(AdminProfile)
admin.site.register(StoreSettings)