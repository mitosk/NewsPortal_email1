from django.urls import path
from .views import (
    NewsList, ArticleList, NewsSearch, ArticleSearch,
    NewsCreate, NewsUpdate, NewsDelete,
    ArticleCreate, ArticleUpdate, ArticleDelete
)

urlpatterns = [
    # Списки
    path('news/', NewsList.as_view(), name='news_list'),
    path('articles/', ArticleList.as_view(), name='article_list'),

    # Поиск и фильтрация
    path('news/search/', NewsSearch.as_view(), name='news_search'),
    path('articles/search/', ArticleSearch.as_view(), name='article_search'),

    # Создание, редактирование, удаление новостей
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    # Создание, редактирование, удаление статей
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]