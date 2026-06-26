# apps.py
from django.apps import AppConfig


class NotesConfig(AppConfig):
    name = "notes"

    def ready(self):
        import notes.signals  # підключаємо сигнали при старті застосунку