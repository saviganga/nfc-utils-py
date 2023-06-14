from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from vcf import utils as vcf_utils

import vobject

VCF_FILE_PATH = "/Users/saviganga/Documents/working-boy/nfc/django/vcf/userInfo"


# Create your models here.
class UserInformation(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(_("phone number"), unique=True, max_length=15)
    email = models.EmailField(_("email address"), max_length=254, unique=True, null=True, blank=True)
    organisation = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    vcarf_file_path = models.CharField(max_length=100, null=True, blank=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added_on']

    def get_full_name(self):

        return f"{self.first_name} {self.last_name}"

    def create_vcard_instance(self):

        # fill the vcard information data
        vcard = vobject.vCard()
        vcard.add('fn').value = self.get_full_name()
        vcard.add('email').value = self.email
        vcard.add('tel').value = self.phone
        vcard.add('org').value = self.organisation
        vcard.add('title').value = self.position

        print(settings.BASE_DIR)

        # Save the vCard to a file
        with open(f"./userInfo/{self.email}.vcf", 'w') as file:
            file.write(vcard.serialize())
        
        self.vcarf_file_path = f"{self.email}.vcf"
        self.save()

        is_uploaded = self.upload_vcard_to_bucket()
        if not is_uploaded:
            return False

        return True
    
    def upload_vcard_to_bucket(self):

        is_uploaded = vcf_utils.upload_vcf_to_bucket(vcf_file=f"./userInfo/{self.email}.vcf", user=self)
        if not is_uploaded:
            return False
        print('uploaded')
        return True







