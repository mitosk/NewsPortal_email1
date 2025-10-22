import django_filters
from django import forms
from .models import Post


class PostFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Название'
    )
    author = django_filters.CharFilter(
        field_name='author__user__username',
        lookup_expr='icontains',
        label='Имя автора'
    )
    date = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = ['name', 'author', 'date']