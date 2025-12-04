from django.apps import AppConfig


class EmbeddingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "embeddings"

    def ready(self):
        from embeddings.signals import register_signal_handlers

        register_signal_handlers()
