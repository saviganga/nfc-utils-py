from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework. views import APIView

from vcf import models as vcf_models
from vcf import serializers as vcf_serializers
from vcf import responses as vcf_responses
from vcf import utils as vcf_utils
from vcf import permissions as vcf_permission

class VCFUserInformationViewSet(ModelViewSet):

    queryset = vcf_models.UserInformation.objects.all()
    serializer_class = vcf_serializers.UserInformationSerializer
    permission_classes = [vcf_permission.UserPermissions | vcf_permission.UserPermissions]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return self.queryset.none()  
        elif self.request.user.is_authenticated and self.request.user.is_staff:
            return self.queryset.all()
        return self.queryset.filter(user=self.request.user)
        

    def list(self, request, *args, **kwargs):

        
        try:
            queryset = self.filter_queryset(self.get_queryset())
            seriaizer = self.get_serializer(queryset, many=True)
            return Response(
                data=vcf_responses.VCFUserInformationResponses().get_user_information_success(data=seriaizer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print(e)
            return Response(
                data=vcf_responses.VCFUserInformationResponses().get_user_information_error(data=seriaizer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):

        mutable_query_dict = request.data.copy()

        # Modify the mutable copy
        mutable_query_dict['key'] = 'value'

        if not mutable_query_dict.get('user'):
            mutable_query_dict['user'] = request.user.id
        
        serializer = self.get_serializer(data=mutable_query_dict)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as invalid_serializer_error:
            print(invalid_serializer_error)
            return Response(
                data=vcf_responses.VCFUserInformationResponses().create_user_information_error(data=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST
            )
        

        self.perform_create(serializer)

        return Response(data=vcf_responses.VCFUserInformationResponses().create_user_information_success(data=serializer.data), status=status.HTTP_201_CREATED)
    
    @action(methods=["get"], detail=True)
    def get_vcf_url(self, request, pk=None):

        instance = self.get_object()

        url = vcf_utils.get_bucket_url(vcf_file=instance.vcarf_file_path)

        return Response(
            data={
                "status": "SUCCESS",
                "message": "Successfully fetched vcard url",
                "data": url
            },
            status=status.HTTP_200_OK
        )
    
    @action(methods=["post"], detail=False)
    def get_signed_vcf_url(self, request, pk=None):

        serializer = vcf_serializers.GetSignedVcardSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as serializer_error:
            print(serializer_error)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Unable to fetch vcf file",
                    "data": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            instance = self.queryset.get(email=serializer.validated_data.get('email'))
        except Exception as user_error:
            print(user_error)
            return Response(
                data={
                    "status": "FAILED",
                    "message": "Unable to fetch vcf file. User not found",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        url = vcf_utils.get_bucket_url(vcf_file=instance.vcarf_file_path)

        return Response(
            data={
                "status": "SUCCESS",
                "message": "Successfully fetched vcard url",
                "data": url
            },
            status=status.HTTP_200_OK
        )

