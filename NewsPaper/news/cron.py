# news/cron.py
from django.utils import timezone
from django.core.mail import send_mail
from .models import Post, Subscription
from django.contrib.auth.models import User

def send_weekly_newsletter():
    """
    Отправляет еженедельную рассылку всем подписчикам.
    Берет новости за последние 7 дней.
    """
    from datetime import timedelta

    one_week_ago = timezone.now() - timedelta(days=7)
    recent_news = Post.objects.filter(post_type='news', created_at__gte=one_week_ago)

    if not recent_news.exists():
        return  # нет новостей за неделю

    # для каждой категории собираем новости и подписчиков
    categories = set(recent_news.values_list('categories', flat=True))
    for category_id in categories:
        category_news = recent_news.filter(categories__id=category_id)
        subscriptions = Subscription.objects.filter(category__id=category_id)

        for sub in subscriptions:
            subject = f"Еженедельная рассылка новостей: {category_news.first().categories}"
            message = "\n\n".join([f"{post.title}\n{post.text[:200]}..." for post in category_news])
            send_mail(
                subject,
                message,
                'newsportal@example.com',  # FROM
                [sub.user.email],
                fail_silently=False
            )
