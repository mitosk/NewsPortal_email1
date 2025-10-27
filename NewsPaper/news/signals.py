from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notify_subscribers  # <-- импортируем задачу Celery

@receiver(post_save, sender=Post)
def send_new_post_email(sender, instance, created, **kwargs):
    if created:
        # вызываем асинхронную задачу Celery для уведомления подписчиков
        notify_subscribers.delay(instance.id)
