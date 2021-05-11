from django.apps import AppConfig
from django.db.models import signals


def create_dynamic_model_fields(sender, **kwargs):
    """Calls the function only if it is defined in the class being prepared"""
    try:
        sender.create_dynamic_fields()
    except AttributeError:
        pass


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def __init__(self, app_name, app_module):
        super().__init__(app_name, app_module)
        # Connect programmatic class adjustment function to the signal
        signals.class_prepared.connect(create_dynamic_model_fields)
