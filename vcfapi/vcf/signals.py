import datetime
from django.db.models.signals import post_save, pre_save

from django.dispatch import receiver
from django.db.models import signals

from vcf import models as vcf_models

@receiver(signals.post_save, sender=vcf_models.UserInformation)
def create_vcard_file(sender, instance, created, **kwargs):

    if created:
        instance.create_vcard_instance()
        print('created')