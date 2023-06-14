from django.apps import AppConfig


class VcfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vcf'

    def ready(self):
        import vcf.signals
