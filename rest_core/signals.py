from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Profile


@receiver(pre_save, sender=Profile, dispatch_uid="create_user_profile")
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=created)


@receiver(pre_save, sender=Profile, dispatch_uid="save_user_profile")
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()