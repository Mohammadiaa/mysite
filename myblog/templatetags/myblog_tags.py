from django import template
from myblog.models import Post
register = template.Library()


@register.simple_tag(name='get_all_posts')
def get_posts():
    return Post.objects.filter(status=1)


@register.filter
def snippet(value, args= 20):
    return value[:args] + '...'

@register.inclusion_tag('myblog/popularposts.html')
def popularposts():
    posts = Post.objects.filter(status = 1).order_by("published_date")[:2]
    return {'posts': posts}