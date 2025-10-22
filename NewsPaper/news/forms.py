from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле категорий необязательным для упрощения
        self.fields['categories'].required = False