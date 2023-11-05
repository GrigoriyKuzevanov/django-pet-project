from django import template
from blog.models import Category, TagPost
import blog.views as views


register = template.Library()

@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.all().prefetch_related('tags')}
