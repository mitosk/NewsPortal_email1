from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Post, Subscription
from .cron import send_weekly_newsletter

@shared_task
def weekly_newsletter_task():
    send_weekly_newsletter()

@shared_task
def notify_subscribers(post_id):
    from .models import Post  # локальный импорт, чтобы избежать циклических зависимостей
    post = Post.objects.get(pk=post_id)
    categories = post.categories.all()
    subscribers = set()

    for category in categories:
        subs = Subscription.objects.filter(category=category)
        for sub in subs:
            subscribers.add(sub.user.email)

    if subscribers:
        subject = f'Новая статья в категории: {", ".join([c.name for c in categories])}'
        message = (
            f'{post.title}\n\n'
            f'{post.text[:300]}...\n\n'
            f'Читать далее: http://127.0.0.1:8000/news/{post.id}/'
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, list(subscribers))

