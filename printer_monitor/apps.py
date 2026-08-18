from django.apps import AppConfig
import os


class PrinterMonitorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "printer_monitor"

    def ready(self):
        # Evita iniciar o scheduler duas vezes durante o auto-reload do runserver
        if os.environ.get("RUN_MAIN") != "true":
            return

        from .scheduler import iniciar_scheduler
        iniciar_scheduler()