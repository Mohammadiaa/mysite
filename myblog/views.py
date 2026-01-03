from django.shortcuts import render, get_object_or_404
from myblog.models import Post
from django.utils import timezone 
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def myblog_view(request, cat_name=None, author_username=None):
    now = timezone.now()
    posts = Post.objects.filter(status= 1, published_date__lte = now)
    if cat_name:
     posts = posts.filter(category__name = cat_name)
    if  author_username:
        posts = posts.filter(author__username = author_username)

    posts = Paginator(posts,3)
    try:
        page_number = request.GET.get('page')
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
         posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    context = {'posts': posts} 
    return render(request, 'myblog/blog-home.html', context)

def myblog_single(request, pid):
    post = get_object_or_404(Post, id=pid, status=1, published_date__lte=timezone.now())
    
    all_posts = list(Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('published_date'))
    current_post_index = all_posts.index(post)

    prev_post = None
    next_post = None

    if current_post_index > 0: #قبلش پست هست
        prev_post = all_posts[current_post_index - 1]

    if current_post_index < len(all_posts) - 1: #بعدش پست هست
        next_post = all_posts[current_post_index + 1]

    context = {
               'post': post,
               'prev_post': prev_post,
               'next_post': next_post} 
    
    post.counted_views += 1
    post.save()  

    
    return render(request, 'myblog/blog-single.html', context)

def test(request):
    return render(request, 'myblog/test.html')

def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name = cat_name)
    context = {'posts': posts}
    return render(request, 'myblog/blog-home.html', context)

def blog_search(request):
    #print(request.__dict__)
    posts = Post.objects.filter(status=1)
    if request.method == "GET":
        #print("get request")
        s_query = request.GET.get('s')

        if s_query:
         posts = posts.filter(content__icontains = s_query )

    context = {'posts': posts}
    return render(request, 'myblog/blog-home.html', context)