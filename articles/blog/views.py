from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView
from .forms import AddPostForm, UploadFileForm
from .models import Category, Post, TagPost, UploadFiles

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'},
]


# def index(request):
#     posts = Post.published.all()
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': 0,
#         }
#     return render(request, 'blog/index2.html', context=data)


class PostHome(ListView):
    # model = Post    # модель для отображения (метод get_queryset)
    template_name = 'blog/index2.html'  # имя шаблона
    context_object_name = 'posts'   # названия переменной для передачи в шаблон списка из модели
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
        }
    
    def get_queryset(self):
        return Post.published.all()
    
    # def get_context_data(self, **kwargs):
    #     """
    #     функция, для передачи динамических данных
    #     передается в момент get запроса
    #     """
    #     context = super().get_context_data(**kwargs)
    #     context['cat_selected'] = int(self.request.GET.get('category_id', 0))
    #     return context


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Post.published.filter(category_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
        }
    return render(request, 'blog/index2.html', context=data)


class PostCategory(ListView):
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
        context['title'] = f'Категория - {category.name}'
        context['menu'] = menu
        context['cat_selected'] = category.pk
        return context


# def handle_uploaded_file(f):
#     """
#     обработчик для загрузки файла
#     """
#     with open(f'uploads/{f.name}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


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

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'blog/post.html', data)

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # # print(form.cleaned_data)
#             # try:
#             #     Post.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Возникла ошибка при добавлении поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
        
#     data = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#         'form': form
#     }
#     return render(request, 'blog/addpage.html', data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'blog/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # # print(form.cleaned_data)
            # try:
            #     Post.objects.create(**form.cleaned_data)
            #     return redirect('home')
            # except:
            #     form.add_error(None, 'Возникла ошибка при добавлении поста')
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Добавление статьи',
            'form': form
        }
        return render(request, 'blog/addpage.html', data)


def contacts(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Post.Status.PUBLISHED)

#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#     return render(request, 'blog/index2.html', context=data)


class TagList(ListView):
    template_name = 'blog/index2.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        self.tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.tag.tags.filter(is_published=Post.Status.PUBLISHED)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Тэг - {self.tag.tag}'
        context['menu'] = menu
        context['cat_selected'] = None
        return context
