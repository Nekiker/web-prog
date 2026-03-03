from django.urls import path, re_path, register_converter
from mandalore import views, converters

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    path('', views.StarshipHome.as_view(), name='home'),
    path('starships/<int:starship_id>/', views.categories, name = 'starships_id'),
    path('starships/<slug:starship_slug>/', views.categories_by_slug, name = 'starships'),
  # re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name = 'archive'),
    path('archive/<year4:year>/', views.archive, name = 'archive'),
    path('about/', views.about, name='about'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('category/<int:cat_id>/', views.ShowCategory.as_view(), name='category'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),

    path('category/<int:cat_id>/', views.ShowCategory.as_view(), name='category'),
    path('post/<slug:post_slug>/edit/', views.UpdatePage.as_view(), name='edit_post'),
    path('post/<slug:post_slug>/delete/', views.DeletePost.as_view(), name='delete_post'),
]
