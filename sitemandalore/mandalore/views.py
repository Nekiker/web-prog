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
from django.views import View
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Starship, Category
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


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

class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

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

@login_required
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

class AddPage(PermissionRequiredMixin, DataMixin, CreateView):
    model = Starship
    form_class = AddPostForm
    template_name = 'mandalore/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'mandalore.add_starship'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавление статьи')
        return {**context, **c_def}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@permission_required(perm='mandalore.view_starship', raise_exception=True)
def contact(request):
    return render(request, 'mandalore/contact.html', {'menu': menu, 'title': 'Обратная связь'})

def login(request):
    return render(request, 'mandalore/login.html', {'menu': menu, 'title': 'Войти'})

class AboutPage(TemplateView):
    template_name = 'mandalore/about.html'
    extra_context = {'menu': menu, 'title': 'О сайте'}

class StarshipHome(ListView):
    template_name = 'mandalore/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Starship.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context




class StarshipHome(DataMixin, ListView):
    template_name = 'mandalore/index.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Starship.objects.filter(is_published=1).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', cat_selected=0)
        return {**context, **c_def}

class ShowCategory(DataMixin, ListView):
    template_name = 'mandalore/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 2

    def get_queryset(self):
        return Starship.objects.filter(
            is_published=1,
            cat_id=self.kwargs['cat_id']
        ).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = Category.objects.get(pk=self.kwargs['cat_id'])
        c_def = self.get_user_context(title=f'Категория: {cat.name}', cat_selected=cat.pk)
        return {**context, **c_def}

class ShowPost(DataMixin, DetailView):
    model = Starship
    template_name = 'mandalore/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_queryset(self):
        return Starship.objects.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        p = context['post']
        c_def = self.get_user_context(title=p.title, cat_selected=p.cat_id)
        return {**context, **c_def}



class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Starship
    form_class = AddPostForm
    template_name = 'mandalore/addpage.html'
    success_url = reverse_lazy('home')
    permission_required = 'mandalore.change_starship'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Редактирование: {self.object.title}')
        return {**context, **c_def}

class DeletePost(PermissionRequiredMixin, DataMixin, DeleteView):
    model = Starship
    template_name = 'mandalore/post_confirm_delete.html'
    success_url = reverse_lazy('home')
    permission_required = 'mandalore.delete_starship'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Удаление: {self.object.title}')
        return {**context, **c_def}

class StarshipHomePaginator(DataMixin, View):
    def get(self, request):
        posts = Starship.objects.filter(is_published=1).select_related('cat')
        paginator = Paginator(posts, 2)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = self.get_user_context(title='Главная страница', cat_selected=0)
        context['page_obj'] = page_obj
        return render(request, 'mandalore/index.html', context)