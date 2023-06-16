from enum import unique
from pyexpat import model
from django.db import models
import uuid
# Create your models here.


class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)



class AuthToken(models.Model):

    id= models.UUIDField(
        help_text="Unique token identifier",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        serialize=True,
        null=False
    )

    token = models.CharField(max_length=50)
    user = models.ForeignKey("userapp.CustomUser", on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, null=True)
    expiry_date = models.DateTimeField(null=True)



# class PublicPrivateToken(models.Model):
#     public_key = models.CharField(max_length=1024)
#     private_key = models.CharField(max_length=1024)
#     user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("public_key", "private_key", "user")