from datetime import datetime
from email.policy import default
from pickle import TRUE
from pyexpat import model
from socket import send_fds
from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import jwt
from .managers import MyUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from decimal import Decimal

from django_otp.models import Device
from django_otp.oath import TOTP
import time
from django.utils import timezone
from django_otp.util import random_hex

from userapp import enums as user_enums
from vcf import models as vcf_models

import uuid


# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(
        _("username"),
        max_length=254,
        help_text=_("The prefereed username"),
        unique=True,
        null=False,
        blank=False
    )
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    first_name = models.CharField(
        _("first name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )

    is_verified = models.BooleanField(
        _("user verified"),
        default=False,
        help_text=_("Designates whether the user is a verified user"),
    )

    spotify_auth = models.JSONField(null=True, blank=True)
    # vcf_info = models.ForeignKey(vcf_models.UserInformation, on_delete=models.SET_NULL, null=True, related_name='uservcf')

    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as "
            "active. Unselect this instead of deleting accounts."
        ),
    )

    gender = models.CharField(
        _("gender"),
        max_length=20,
        blank=True,
        choices=user_enums.GENDER,
        help_text=_("User gender"),
    )
    bio = models.TextField(
        max_length=250, blank=True, null=True, help_text=_("User bio")
    )
    
    # picture = models.ImageField(
    #     blank=True, null=True, upload_to=file_services.renameProfilePicture, help_text=_("User picture")
    # )

    updated_on = models.DateTimeField(_("updated on"), auto_now=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    social_login = models.BooleanField(null=True, blank=True, default=False)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "user_name"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ["-updated_on", "-date_joined"]

    def __unicode__(self):
        return f"{self.user_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()
        full_name = f"{first_name} {last_name}"
        return full_name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True
    

# class UserOTPDevice(Device):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     secret_key = models.CharField(
#         max_length=40,
#         default="a17d71c773b44b96b0486b9b349b340223bf14e3",
#         help_text="Hex-encoded secret key to generate totp tokens.",
#     )
#     last_verified_counter = models.BigIntegerField(
#         default=-1,
#         help_text=(
#             "The counter value of the latest verified token."
#             "The next token must be at a higher counter value."
#             "It makes sure a token is used only once."
#         ),
#     )

#     step = 300
#     digits = 6

#     class Meta(Device.Meta):
#         verbose_name = "Verification Device"

#     def totp_obj(self):
#         totp = TOTP(
#             key=bytes.fromhex(self.secret_key), step=self.step, digits=self.digits
#         )
#         totp.time = time.time()
#         return totp

#     def generate_token(self):
#         totp = self.totp_obj()
#         token = str(totp.token()).zfill(self.digits)

#         message = _(
#             f"TruQ verification OTP for {self.user.first_name} is {token}. "
#             f"It is valid for {self.step // 60} minutes."
#         )
#         return token, message

#     def verify_token(self, inp_token: int, tolerance=0):
#         totp = self.totp_obj()
#         if (totp.t() > self.last_verified_counter) and (
#             totp.verify(inp_token, tolerance=tolerance)
#         ):
#             self.last_verified_counter = totp.t()
#             self.save()
#             return True
#         else:
#             return False


# class Preferences(models.Model):    
#     user = models.OneToOneField(
#         "user.CustomUser", on_delete=models.CASCADE, related_name="preferences"
#     )
#     send_email = models.BooleanField(default=True)
#     send_sms = models.BooleanField(default=False)
#     send_push_notification = models.BooleanField(default=True)


# class EncryptionStore(models.Model):
#     """
#         This stores the encrypted  values to our enabled user public key Authentication
#     """
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     user = models.OneToOneField(
#         "user.CustomUser", on_delete=models.CASCADE, related_name='user_pk_key')

#     cypher_text = models.CharField( unique=True, max_length=100)
#     cypher_dict = models.JSONField(max_length=100, help_text="User wallet cypher", default=dict)
#     pub_key = models.CharField( unique=True, max_length=100)
   
#     created_on = models.DateTimeField(auto_now_add=True)
#     updated_on = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "EncryptionStore"

