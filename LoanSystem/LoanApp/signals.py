from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import  Payment





@receiver(post_save, sender=Payment)
def post_save_payment(sender, instance, created, **kwargs):
    if created:
        if instance.balance == 0:
            instance.loan.status = "Paid"

        if instance.Amount >= 300 and instance.Type == "Processing Fee":
            instance.loan.status = "Disbursed"
