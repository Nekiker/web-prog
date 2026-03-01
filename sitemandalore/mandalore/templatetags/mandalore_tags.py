from django import template
from mandalore import views
from django.db.models import Count
from mandalore.models import Category, TagPost

register = template.Library()

@register.inclusion_tag('mandalore/list_tags.html')
def show_all_tags():
    return {"tags": TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}

@register.simple_tag()
def get_categories():
    return views.cats_db

@register.inclusion_tag('mandalore/list_categories.html')
def show_categories(cat_selected_id=0):
    cats = Category.objects.annotate(total=Count("posts")).filter(total__gt=0)
    return {"cats": cats, "cat_selected": cat_selected_id}