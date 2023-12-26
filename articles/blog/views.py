from typing import Any
from django.conf import settings

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db import models
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, redirect, render
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)

from blog.utils import DataMixin

from .forms import AddPostForm, UploadFileForm, AddCommentForm
from .models import Category, Post, TagPost, UploadFiles

menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "addpage"},
    {"title": "Обратная связь", "url_name": "contacts"},
    {"title": "Войти", "url_name": "login"},
]


class PostHome(DataMixin, ListView):
    # model = Post    # модель для отображения (метод get_queryset)
    template_name = "blog/index2.html"  # имя шаблона
    context_object_name = (
        "posts"  # названия переменной для передачи в шаблон списка из модели
    )
    title_page = "Главная страница"
    cat_selected = 0

    def get_queryset(self):
        return Post.published.all()


class PostCategory(DataMixin, ListView):
    template_name = "blog/index2.html"
    context_object_name = "posts"
    allow_empty = (
        False,  # при пустом списке сontext['posts'] генерируется исключение 404
    )

    def get_queryset(self):
        return Post.published.filter(
            category__slug=self.kwargs["cat_slug"]
        )  # cat_slug из url blog/<cat_slug>

    def get_context_data(self, **kwargs):
        """
        функция, для передачи динамических данных
        передается в момент get запроса
        """
        context = super().get_context_data(**kwargs)
        category = context["posts"][0].category
        return self.get_mixin_context(
            context, title=f"Категория - {category.name}", cat_selected=category.pk
        )


@login_required
def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "blog/about.html",
        {"title": "О сайте", "menu": menu, "page_obj": page_obj},
    )


class ShowPost(DataMixin, DetailView, CreateView):
    model = Post
    form_class = AddCommentForm
    template_name = "blog/post.html"
    slug_url_kwarg = "post_slug"  # название slug переменной из запроса в urls
    context_object_name = 'post'
  
    def get_success_url(self):
        kwargs={'post_slug': self.get_object().slug}
        return reverse_lazy('post', kwargs=kwargs)

    def form_valid(self, form):
        c = form.save(commit=False)
        c.author = self.request.user
        c.post = self.get_object()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title, form=AddCommentForm, default_img=settings.DEFAULT_USER_IMAGE)

    def get_object(self, queryset=None):
        return get_object_or_404(Post.published.prefetch_related('comments').annotate(total_comments=Count('comments')), slug=self.kwargs[self.slug_url_kwarg])

    
class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    # model = Post
    # fields = ['title', 'slug', 'image', 'content', 'is_published', 'category', 'author']
    template_name = "blog/addpage.html"  # по умолчанию в шаблон форма передается через переменную form
    success_url = reverse_lazy(
        "home"
    )  # функция revers_lazy возвращает полный маршрут по имени из urls path в момент вызова
    # в CreateView берется из метода get_absolute_url класса связанной модели
    title_page = "Добавление поста"
    permission_required = 'blog.add_post'   # <приложение>.<действие>_<таблица>

    def form_valid(
        self, form
    ):  # при отправлении формы, в post добавляется автор - пользователь который делает запрос
        p = form.save(commit=False)
        p.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Post
    fields = ["title", "content", "image", "is_published", "category"]
    template_name = "blog/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Редактирование поста"
    permission_required = 'blog.change_post'


class DeletePage(DataMixin, DeleteView):
    model = Post
    template_name = "blog/deletepage.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление поста"


def contacts(request):
    return HttpResponse("Обратная связь")


def login(request):
    return HttpResponse("Авторизация")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class TagList(DataMixin, ListView):
    template_name = "blog/index2.html"
    context_object_name = "posts"

    def get_queryset(self):
        self.tag = TagPost.objects.get(slug=self.kwargs["tag_slug"])
        return self.tag.tags.filter(is_published=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=f"Тэг - {self.tag.tag}")
