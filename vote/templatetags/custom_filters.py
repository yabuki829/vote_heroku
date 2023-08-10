from django import template
from ..models import Blog
register = template.Library()

@register.filter
def get_news(value):
    blogs = Blog.objects.all().order_by('-createdAt')[:3]
    return blogs

@register.filter
def add_two(value):
    return value + 2

@register.filter
def get_item(list, index):
    return list[index]
    
