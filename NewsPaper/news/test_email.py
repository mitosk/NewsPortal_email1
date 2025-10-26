import django
import os

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
django.setup()

from django.contrib.auth.models import User
from news.models import Category, Post, Subscription
from news.signals import send_new_post_email

# 1️⃣ Создаём тестового пользователя
user, created = User.objects.get_or_create(
    username='test_user',
    defaults={'email': 'test_user@example.com', 'password': '123456'}
)

# 2️⃣ Создаём тестовую категорию
category, created = Category.objects.get_or_create(name='Тестовая категория')

# 3️⃣ Подписываем пользователя на категорию
Subscription.objects.get_or_create(user=user, category=category)

# 4️⃣ Создаём тестовый пост
post = Post.objects.create(
    title='Тестовая статья для рассылки',
    text='Это тестовая статья, которая должна отправиться подписчику.',
    post_type='news'
)
post.categories.add(category)

# 5️⃣ Вызов сигнала вручную
send_new_post_email(Post, post, created=True)

print("Тестовая рассылка выполнена. Проверьте email пользователя или консоль.")