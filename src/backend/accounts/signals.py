from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AccountMeter

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def post_save_create_account_meter(sender, instance, created, *args, **kwargs):
    if created:
        AccountMeter.objects.create(
            account=instance,
            house_number=f'Area 47/4/{instance.pk}'
        )
        print(AccountMeter)