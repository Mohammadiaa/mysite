from django import template
from myblog.models import Post
register = template.Library()





@register.simple_tag(name='get_all_posts')
def get_posts():
    return Post.objects.filter(status=1)