# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductOrder, Notification

@receiver(post_save, sender=ProductOrder)
def create_order_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            message=f"تم إنشاء طلب جديد من {instance.full_name} لمنتج {instance.product.name}"
        )
