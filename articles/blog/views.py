from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .forms import AddPostForm, UploadFileForm
from .models import Category, Post, TagPost, UploadFiles
from blog.utils import DataMixin

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'},
]


class PostHome(DataMixin, ListView):
    # model = Post    # модель для отображения (метод get_queryset)
    template_name = 'blog/index2.html'  # имя шаблона
    context_object_name = 'posts'   # названия переменной для передачи в шаблон списка из модели
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all()
    

class PostCategory(DataMixin, ListView):
    template_name = 'blog/index2.html'
    context_object_name = 'posts'
    allow_empty = False     # при пустом списке сontext['posts'] генерируется исключение 404

    def get_queryset(self):
        return Post.published.filter(category__slug=self.kwargs['cat_slug'])    # cat_slug из url blog/<cat_slug>
    
    def get_context_data(self, **kwargs):
        """
        функция, для передачи динамических данных
        передается в момент get запроса
        """
        context = super().get_context_data(**kwargs)
        category = context['posts'][0].category
        return self.get_mixin_context(context, title=f'Категория - {category.name}', cat_selected=category.pk)


def about(request):
    if request.method == 'POST':
        # handle_uploaded_file(request.FILES['file_upload'])  # ключ 'file_upload' в html форме атрибут name='file_upload'
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'blog/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})


class ShowPost(DataMixin, DetailView):
    # model = Post
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'    # название slug переменной из запроса в urls
    # context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
    
    def get_object(self, queryset=None):
        return get_object_or_404(Post.published, slug=self.kwargs[self.slug_url_kwarg])


class AddPage(DataMixin, CreateView):
    form_class = AddPostForm
    # model = Post
    # fields = ['title', 'slug', 'image', 'content', 'is_published', 'category', 'author']
    template_name = 'blog/addpage.html'     # по умолчанию в шаблон форма передается через переменную form
    success_url = reverse_lazy('home')   # функция revers_lazy возвращает полный маршрут по имени из urls path в момент вызова
                                           # в CreateView берется из метода get_absolute_url класса связанной модели
    title_page = 'Добавление поста'


class UpdatePage(DataMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published', 'category']
    template_name = 'blog/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование поста'


class DeletePage(DataMixin, DeleteView):
    model = Post
    template_name = 'blog/deletepage.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление поста'


def contacts(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class TagList(DataMixin, ListView):
    template_name = 'blog/index2.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f'Тэг - {self.tag.tag}')
