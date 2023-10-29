from django.db import router
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'vcf'

router = DefaultRouter()

# router.register("booking-related-services", views.BookingServiceRelatedServicesViewSet)
router.register("vcf-user-info", views.VCFUserInformationViewSet)

urlpatterns = [
    
]

urlpatterns += router.urls
