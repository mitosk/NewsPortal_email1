from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Post, Subscription

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Добро пожаловать в NewsPortal!',
            f'Здравствуйте, {instance.username}!\n\nДобро пожаловать в наш новостной портал. '
            'Теперь вы можете подписываться на любимые категории и получать свежие статьи на почту!',
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
        )

@receiver(post_save, sender=Post)
def send_new_post_email(sender, instance, created, **kwargs):
    if not created:
        return

    categories = instance.categories.all()  # <-- исправлено
    subscribers = set()

    for category in categories:
        subs = Subscription.objects.filter(category=category)
        for sub in subs:
            subscribers.add(sub.user.email)

    if subscribers:
        subject = f'Новая статья в категории: {", ".join([c.name for c in categories])}'
        message = (
            f'{instance.title}\n\n'
            f'{instance.text[:300]}...\n\n'
            f'Читать далее: http://127.0.0.1:8000/news/{instance.id}/'
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(subscribers))