from django.apps import AppConfig

class RelationshipAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LibraryProject.bookshelf'

    def ready(self):
        from . import signals  # noqa: F401