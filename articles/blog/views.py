from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from blog.models import Category, Post, TagPost

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'addpage'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Заголовок статьи 1', 'content': 'Содержимое статьи 1', 'is_published': True},
    {'id': 2, 'title': 'Заголовок статьи 2', 'content': 'Содержимое статьи 2', 'is_published': True},
    {'id': 3, 'title': 'Заголовок статьи 3', 'content': 'Содержимое статьи 3', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Учеба', 'description': 'Всё об учебных делах', 'class': 'red-bage'},
    {'id': 2, 'name': 'Рецепты', 'description': 'Рецепты любимых блюд', 'class': 'blue-bage'},
    {'id': 3, 'name': 'Beauty', 'description': 'Индустрия красоты', 'class': 'green-bage'},
]

def index(request):
    posts = Post.published.all()
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
        }
    return render(request, 'blog/index2.html', context=data)

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

def about(request):
    return render(request, 'blog/about.html', {'title': 'О сайте', 'menu': menu})

def show_post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'blog/post.html', data)

def addpage(request):
    return render(request, 'blog/addpage.html', {'menu': menu, 'title': 'Добавление статьи'})

def contacts(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED)

    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'blog/index2.html', context=data)
