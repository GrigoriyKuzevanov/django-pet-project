from django import forms
from .models import Category, Author, Post


class AddPostForm(forms.Form):
    """
    Класс для формы добавления нового поста
    """
    title = forms.CharField(max_length=255, label='Заголовок') # для передачи атрибутов тэга: widget=forms.TextInput(attrs={'class': span3}) (пример)
    slug = forms.SlugField(max_length=255, label='Слаг')
    content = forms.CharField(widget=forms.Textarea(), required=False, label='Текст поста')
    is_published = forms.BooleanField(required=False, label='Опубликовать', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=False, label='Автор', empty_label='Автор не выбран')    # required=False делает поле необязательным
