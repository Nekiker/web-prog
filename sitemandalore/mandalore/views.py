from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from .models import Starship


menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

cats_db = [
    {'id': 1, 'name': 'Лёгкие корабли'},
    {'id': 2, 'name': 'Грузовые корабли'},
    {'id': 3, 'name': 'Истребители'},
]

data_db = [
    {'id': 1, 'title': 'Razor Crest', 'content': 'Описание Razor Crest', 'is_published': True,  'cat_id': 1},
    {'id': 2, 'title': 'Slave I', 'content': 'Описание Slave I', 'is_published': False,       'cat_id': 1},
    {'id': 3, 'title': 'Millennium Falcon', 'content': 'Описание Falcon', 'is_published': True,'cat_id': 2},
]

def show_category(request, cat_id):
    posts = [p for p in data_db if p.get('cat_id') == cat_id]

    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': posts,
        'cat_selected': cat_id,
    }
    return render(request, 'mandalore/index.html', context=data)

def show_post(request, post_slug):
    post = get_object_or_404(Starship, slug=post_slug)

    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }
    return render(request, 'mandalore/post.html', context=data)

def index(request):
    posts = Starship.objects.filter(is_published=True)
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'mandalore/index.html', context=data)

def about(request):
    return render(request, 'mandalore/about.html', {'title': 'О сайте', 'menu': menu, 'cat_selected': 0})

def categories(request, starship_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >id:{starship_id}</p>")

def categories_by_slug(request, starship_slug):
    if request.GET:
        print(request.GET)

    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug: {starship_slug}</p>")

def archive(request, year):
    if year > 2025:
        url_redirect = reverse('starships', args=('weapon', ))
        return redirect(url_redirect, permanent=True)

    return HttpResponse(f"<h1>Архив по годам</h1><p >{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

# Create your views here.
