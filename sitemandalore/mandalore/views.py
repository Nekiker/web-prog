from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return HttpResponse("Страница приложения mandalore.")


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
