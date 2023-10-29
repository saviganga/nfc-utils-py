#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from opentelemetry.instrumentation.django import DjangoInstrumentor
import uptrace


def main():
    """Run administrative tasks."""
    uptrace.configure_opentelemetry(
        # Copy DSN here or use UPTRACE_DSN env var.
        dsn="https://J5M0tq8CTRv0idzvrCDczA@api.uptrace.dev/2658",
        service_name="vcfService",
        service_version="v1.0.0",
    )
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vcfapi.settings')
    DjangoInstrumentor().instrument()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
