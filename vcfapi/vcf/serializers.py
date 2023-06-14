from rest_framework import serializers

from vcf import models as vcf_models

class UserInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = vcf_models.UserInformation
        fields = '__all__'

class GetSignedVcardSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)