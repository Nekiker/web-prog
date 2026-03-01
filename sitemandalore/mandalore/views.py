from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404, render
from .models import Starship
from .forms import AddPostForm
from .forms import UploadFileForm
from .models import Starship, PublishStatus
from django.db import IntegrityError
import uuid
from .models import UploadFiles

menu = [
    {'title': "Главная", 'url_name': 'home'},
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'addpage'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]

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

def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]

        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())

    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'mandalore/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})

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

from django.shortcuts import render, redirect
from .forms import AddPostForm

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()

    return render(request, 'mandalore/addpage.html',
                  {'menu': menu, 'title': 'Добавление статьи', 'form': form})

def contact(request):
    return render(request, 'mandalore/contact.html', {'menu': menu, 'title': 'Обратная связь'})

def login(request):
    return render(request, 'mandalore/login.html', {'menu': menu, 'title': 'Войти'})