from django.urls import path
from . import views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,        # правильное имя класса для удаления
    ProfileUpdateView,
    become_author,
    NewsList,
    ArticleList,
    NewsSearch,
    ArticleSearch,
    NewsCreate,
    NewsUpdate,
    NewsDelete,
    ArticleCreate,
    ArticleUpdate,
    ArticleDelete,
    NewsByCategory,
    ArticlesByCategory,
    CategoryList
)

urlpatterns = [
    # Посты
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

    # Профиль
    path('profile/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('become-author/', become_author, name='become_author'),

    # Новости и статьи
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view(), name='article_list'),
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

    # Новости/статьи по категориям
    path('news/category/<int:category_id>/', NewsByCategory.as_view(), name='news_by_category'),
    path('articles/category/<int:category_id>/', ArticlesByCategory.as_view(), name='articles_by_category'),

    # Список категорий
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('subscribe/<int:category_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe, name='unsubscribe'),

    path('subscribe/<int:category_id>/', views.subscribe, name='subscribe'),
    path('unsubscribe/<int:category_id>/', views.unsubscribe, name='unsubscribe'),
    path('category/<int:category_id>/', views.NewsByCategory.as_view(), name='news_by_category'),
]