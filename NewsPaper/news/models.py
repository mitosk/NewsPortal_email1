from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_total = Post.objects.filter(author=self).aggregate(total=Sum('rating'))['total'] or 0
        comments_by_author = Comment.objects.filter(user=self.user).aggregate(total=Sum('rating'))['total'] or 0
        comments_on_author_posts = Comment.objects.filter(post__author=self).aggregate(total=Sum('rating'))['total'] or 0
        self.rating = posts_total * 3 + comments_by_author + comments_on_author_posts
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()  # Убедитесь что поле называется text
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text

    def __str__(self):
        return self.title

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('post', 'category')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating = models.F('rating') + 1
        self.save(update_fields=['rating'])
        self.refresh_from_db()

    def dislike(self):
        self.rating = models.F('rating') - 1
        self.save(update_fields=['rating'])
        self.refresh_from_db()
