from django import template
from myblog.models import Post,Comment
from myblog.models import Category
register = template.Library()


@register.simple_tag(name='get_all_posts')
def get_posts():
    return Post.objects.filter(status=1)

@register.simple_tag(name='comments_count')
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()

@register.filter
def snippet(value, args= 20):
    return value[:args] + '...'

@register.inclusion_tag('myblog/blog-popular-posts.html')
def latestposts(arg=3):
    posts = Post.objects.filter(status = 1).order_by("-published_date")[:arg]
    return {'posts': posts}

@register.inclusion_tag('myblog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {'categories':cat_dict}

@register.inclusion_tag('website/blog-recent-posts.html')
def latest_posts(count=6):
    posts = Post.objects.filter(status=1).order_by('-published_date')[:count]
    return {'posts': posts}