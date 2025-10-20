from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    # Получаем все новости и статьи, сортируем от новых к старым
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'posts': posts})

def news_detail(request, news_id):
    # Получаем конкретную новость/статью по ID
    post = get_object_or_404(Post, id=news_id)
    return render(request, 'news/news_detail.html', {'post': post})