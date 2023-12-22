from django import template
from django.db.models import Count

import blog.views as views
from blog.models import Category, TagPost
from blog.utils import menu

register = template.Library()

@register.inclusion_tag('blog/list_categories.html')
def show_categories(cat_selected=0):
    # cats = Category.objects.all()
    cats = Category.objects.annotate(total_posts=Count('posts')).filter(total_posts__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('blog/list_tags.html')
def show_all_tags():
    tags = TagPost.objects.prefetch_related('tags').annotate(total_posts=Count('tags')).filter(total_posts__gt=0).order_by('-total_posts')[:5]
    return {'tags': tags}
