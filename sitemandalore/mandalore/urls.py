from django.urls import path, re_path, register_converter
from mandalore import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.index, name = 'home'),
    path('starships/<int:starship_id>/', views.categories, name = 'starships_id'),
    path('starships/<slug:starship_slug>/', views.categories_by_slug, name = 'starships'),
  # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name = 'archive'),
    path('archive/<year4:year>/', views.archive, name = 'archive'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),

]
