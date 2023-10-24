from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

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
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cat_selected': 0,
        }
    return render(request, 'blog/index.html', context=data)

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
        }
    return render(request, 'blog/index.html', context=data)

def about(request):
    return render(request, 'blog/about.html', {'title': 'О сайте', 'menu': menu})

def show_post(request, post_id):
    return HttpResponse(f'Отображение статьи с id: {post_id}')

def addpage(request):
    return HttpResponse('Добавление статьи')

def contacts(request):
    return HttpResponse('Обратная связь')

def login(request):
    return HttpResponse('Авторизация')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")
