# news/filters.py
import django_filters
from django import forms
from .models import Post, Category


class PostFilter(django_filters.FilterSet):
    # Поиск по названию
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название содержит:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название...'})
    )

    # Поиск по автору
    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора содержит:',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя автора...'})
    )

    # Фильтр по дате
    date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Опубликовано после:',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    # Фильтр по категории
    category = django_filters.ModelChoiceFilter(
        field_name='categories',
        queryset=Category.objects.all(),
        label='Категория:',
        empty_label='Все категории',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date', 'category']