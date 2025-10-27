from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from .models import Post, Category, Author, Subscription
from .filters import PostFilter
from .forms import PostForm

# 🔹 Импорт Celery-задачи
from .tasks import notify_subscribers


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author.user or self.request.user.is_superuser


class PostListView(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'


class PostDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'category']
    template_name = 'news/post_form.html'
    permission_required = 'news.add_post'


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'text', 'category']
    template_name = 'news/post_edit.html'
    permission_required = 'news.change_post'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'news/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def become_author(request):
    author_group, _ = Group.objects.get_or_create(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(request.user)
    return redirect('/')


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


# 🔹 Асинхронная рассылка после создания новости
class NewsCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/news_edit.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'

        # Устанавливаем автора
        try:
            user = User.objects.get(username='default_author')
            author = Author.objects.get(user=user)
        except (User.DoesNotExist, Author.DoesNotExist):
            author = Author.objects.first()
            if not author:
                user = User.objects.create_user(username='auto_author')
                author = Author.objects.create(user=user)
        post.author = author

        response = super().form_valid(form)

        # 🔸 Асинхронно уведомляем подписчиков через Celery
        notify_subscribers.delay(post.id)

        return response


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


# 🔹 Аналогично добавим рассылку и для статей
class ArticleCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/article_edit.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        article.post_type = 'article'

        try:
            user = User.objects.get(username='default_author')
            author = Author.objects.get(user=user)
        except (User.DoesNotExist, Author.DoesNotExist):
            author = Author.objects.first()
            if not author:
                user = User.objects.create_user(username='auto_author')
                author = Author.objects.create(user=user)
        article.author = author

        response = super().form_valid(form)

        # 🔸 Рассылка подписчикам через Celery
        notify_subscribers.delay(article.id)

        return response


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


class NewsByCategory(ListView):
    model = Post
    template_name = 'news/news_by_category.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['category_id'])
        return Post.objects.filter(post_type='news', categories=self.category).order_by('-created_at')

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
        return Post.objects.filter(post_type='article', categories=self.category).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories_with_counts = []
        total_news = 0
        total_articles = 0

        for category in context['categories']:
            news_count = Post.objects.filter(post_type='news', categories=category).count()
            articles_count = Post.objects.filter(post_type='article', categories=category).count()

            categories_with_counts.append({
                'category': category,
                'news_count': news_count,
                'articles_count': articles_count
            })

            total_news += news_count
            total_articles += articles_count

        context['categories_with_counts'] = categories_with_counts
        context['total_news'] = total_news
        context['total_articles'] = total_articles
        return context


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.get_or_create(user=request.user, category=category)
    return redirect('category_list')


@login_required
def unsubscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    Subscription.objects.filter(user=request.user, category=category).delete()
    return redirect('category_list')
