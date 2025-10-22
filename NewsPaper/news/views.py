from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404  # ← ДОБАВИТЬ ЭТОТ ИМПОРТ
from .models import Post, Category  # ← ДОБАВИТЬ Category В ИМПОРТ
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'news'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticleList(ListView):
    model = Post
    template_name = 'news/article_list.html'
    context_object_name = 'articles'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class NewsSearch(ListView):
    model = Post
    template_name = 'news/news_search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='news').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticleSearch(ListView):
    model = Post
    template_name = 'news/article_search.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(post_type='article').order_by('-created_at')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'news/news_delete.html'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='news')


class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'news/article_delete.html'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(post_type='article')


# Альтернативные представления (используют ID вместо slug)
class NewsByCategory(ListView):
    model = Post
    template_name = 'news/news_by_category.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Post.objects.filter(
            post_type='news',
            categories=self.category
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ArticlesByCategory(ListView):
    model = Post
    template_name = 'news/articles_by_category.html'
    context_object_name = 'articles'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Post.objects.filter(
            post_type='article',
            categories=self.category
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


# ДОБАВИТЬ КЛАСС CategoryList
class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Вручную считаем количество постов для каждой категории
        categories_with_counts = []
        for category in context['categories']:
            news_count = Post.objects.filter(
                post_type='news',
                categories=category
            ).count()
            articles_count = Post.objects.filter(
                post_type='article',
                categories=category
            ).count()
            categories_with_counts.append({
                'category': category,
                'news_count': news_count,
                'articles_count': articles_count
            })
        context['categories_with_counts'] = categories_with_counts
        return context