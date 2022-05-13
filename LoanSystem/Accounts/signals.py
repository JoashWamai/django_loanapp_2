from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Profile

@receiver(pre_save, sender=Profile)
def pre_save_profile(sender, instance, **kwargs):
    if instance.Category == "Field Officer":
        officer = Group.objects.get(name="officer")
        instance.user.groups.add(officer)
    elif instance.Category == "Supervisor":
        supervisor = Group.objects.get(name="supervisor")
        instance.user.groups.add(supervisor)
    else:
        administrator = Group.objects.get(name="administrator")
        instance.user.groups.add(administrator)

    print("New user created", instance.Category)