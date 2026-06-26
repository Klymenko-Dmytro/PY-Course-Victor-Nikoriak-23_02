# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Note  # Назва вашої моделі нотаток
from .utils import send_telegram_message

@receiver(post_save, sender=Note)
def notify_new_note(sender, instance, created, **kwargs):
    if created:  # Перевірка, що нотатка саме створена, а не оновлена
        text_message = f"📝 *Нова нотатка!*\n\n*Заголовок:* {instance.title}\n\n{instance.text}"
        send_telegram_message(text_message)
