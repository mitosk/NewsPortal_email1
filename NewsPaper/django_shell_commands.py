print("=== НАЧАЛО ВЫПОЛНЕНИЯ КОМАНД DJANGO SHELL ===")


from django.contrib.auth.models import User
from news.models import Author, Category, Post, PostCategory, Comment

try:
    user1 = User.objects.create_user('user1')
    user2 = User.objects.create_user('user2')
    print("1. Пользователи созданы успешно")
except:
    user1 = User.objects.get(username='user1')
    user2 = User.objects.get(username='user2')
    print("1. Пользователи уже существуют, получены из базы")

try:
    author1 = Author.objects.create(user=user1)
    author2 = Author.objects.create(user=user2)
    print("2. Авторы созданы успешно")
except:
    author1 = Author.objects.get(user=user1)
    author2 = Author.objects.get(user=user2)
    print("2. Авторы уже существуют, получены из базы")

categories_data = [
    {'name': 'Спорт'},
    {'name': 'Политика'},
    {'name': 'Образование'},
    {'name': 'Технологии'}
]

categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(name=cat_data['name'])
    categories.append(category)
    if created:
        print(f"3. Создана категория: {cat_data['name']}")
    else:
        print(f"3. Категория уже существует: {cat_data['name']}")

category_sport, category_politics, category_education, category_tech = categories

Post.objects.filter(title='Первая статья о спорте').delete()
Post.objects.filter(title='Вторая статья о политике').delete()
Post.objects.filter(title='Новость об образовании').delete()

try:
    post1 = Post.objects.create(
        author=author1,
        post_type=Post.ARTICLE,
        title='Первая статья о спорте',
        text='Это полный текст первой статьи о спорте. ' * 10
    )
    print("4. Создана статья 1")
except Exception as e:
    print(f"4. Ошибка создания статьи 1: {e}")

try:
    post2 = Post.objects.create(
        author=author2,
        post_type=Post.ARTICLE,
        title='Вторая статья о политике',
        text='Это полный текст второй статьи о политике. ' * 10
    )
    print("5. Создана статья 2")
except Exception as e:
    print(f"5. Ошибка создания статьи 2: {e}")

try:
    post3 = Post.objects.create(
        author=author1,
        post_type=Post.NEWS,
        title='Новость об образовании',
        text='Это полный текст новости об образовании. ' * 10
    )
    print("6. Создана новость")
except Exception as e:
    print(f"6. Ошибка создания новости: {e}")

post1 = Post.objects.get(title='Первая статья о спорте')
post2 = Post.objects.get(title='Вторая статья о политике')
post3 = Post.objects.get(title='Новость об образовании')

post_categories_data = [
    (post1, category_sport),
    (post1, category_tech),
    (post2, category_politics),
    (post3, category_education),
    (post3, category_tech)
]

for post, category in post_categories_data:
    if not PostCategory.objects.filter(post=post, category=category).exists():
        PostCategory.objects.create(post=post, category=category)
        print(f"7. Назначена категория '{category.name}' для '{post.title}'")
    else:
        print(f"7. Связь уже существует: '{post.title}' - '{category.name}'")

Comment.objects.all().delete()

comments_data = [
    (post1, user2, 'Отличная статья о спорте!'),
    (post1, user1, 'Очень интересно, спасибо!'),
    (post2, user1, 'Хороший анализ политической ситуации'),
    (post3, user2, 'Важная новость для образования')
]

comments = []
for i, (post, user, text) in enumerate(comments_data, 1):
    comment = Comment.objects.create(
        post=post,
        user=user,
        text=text
    )
    comments.append(comment)
    print(f"8. Создан комментарий {i}")

comment1, comment2, comment3, comment4 = comments

print("9. Изменение рейтингов постов...")

post1.rating = 0
post2.rating = 0
post3.rating = 0
post1.save()
post2.save()
post3.save()

post1.like()
post1.like()
post1.like()
post1.dislike()
print(f"   Post1: рейтинг = {post1.rating}")

post2.like()
post2.dislike()
post2.dislike()
print(f"   Post2: рейтинг = {post2.rating}")

post3.like()
post3.like()
post3.like()
post3.like()
post3.like()
print(f"   Post3: рейтинг = {post3.rating}")

print("10. Изменение рейтингов комментариев...")

for comment in comments:
    comment.rating = 0
    comment.save()

comment1.like()
comment1.like()
comment1.dislike()
print(f"   Comment1: рейтинг = {comment1.rating}")

comment2.like()
print(f"   Comment2: рейтинг = {comment2.rating}")

comment3.like()
comment3.like()
comment3.like()
print(f"   Comment3: рейтинг = {comment3.rating}")

comment4.like()
comment4.dislike()
print(f"   Comment4: рейтинг = {comment4.rating}")

print("11. Обновление рейтингов авторов...")
author1.update_rating()
author2.update_rating()
print(f"   Рейтинг {author1.user.username}: {author1.rating}")
print(f"   Рейтинг {author2.user.username}: {author2.rating}")

best_author = Author.objects.order_by('-rating').first()
print(f"12. ЛУЧШИЙ ПОЛЬЗОВАТЕЛЬ: {best_author.user.username}, рейтинг: {best_author.rating}")

best_post = Post.objects.order_by('-rating').first()
print(f"13. ЛУЧШАЯ СТАТЬЯ:")
print(f"   Дата добавления: {best_post.created_at}")
print(f"   Автор: {best_post.author.user.username}")
print(f"   Рейтинг: {best_post.rating}")
print(f"   Заголовок: {best_post.title}")
print(f"   Превью: {best_post.preview()}")

print("14. КОММЕНТАРИИ К ЛУЧШЕЙ СТАТЬЕ:")
comments_to_best_post = Comment.objects.filter(post=best_post)
if comments_to_best_post.exists():
    for i, comment in enumerate(comments_to_best_post, 1):
        print(f"   Комментарий {i}:")
        print(f"      Дата: {comment.created_at}")
        print(f"      Пользователь: {comment.user.username}")
        print(f"      Рейтинг: {comment.rating}")
        print(f"      Текст: {comment.text}")
        print()
else:
    print("   Нет комментариев к этой статье")

print("=== ВЫПОЛНЕНИЕ КОМАНД ЗАВЕРШЕНО ===")