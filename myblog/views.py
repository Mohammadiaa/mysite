from django.shortcuts import render, get_object_or_404, redirect
from myblog.models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from myblog.forms import CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

def myblog_view(request, cat_name=None, author_username=None, tag_name=None):
    now = timezone.now()
    posts = Post.objects.filter(
        status=1, published_date__lte=now).order_by('-published_date')

    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)
    if tag_name:
        posts = posts.filter(tags__name=tag_name)

    posts = Paginator(posts, 3)
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

    if post.login_require and not request.user.is_authenticated:
        # return redirect('accounts:login') 
         return redirect(reverse('accounts:login'))

    comments = Comment.objects.filter(post=post, approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            
            if request.user.is_authenticated:
                comment.name = request.user.first_name
                comment.email = request.user.email
            comment.save()
            messages.success(request, 'your comment submitted successfully')
        else:
            messages.error(request, 'your comment did not submit')
    else:
        form = CommentForm()

    all_posts = list(Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('published_date'))
    current_post_index = all_posts.index(post)

    prev_post = None
    next_post = None

    if current_post_index > 0:
        prev_post = all_posts[current_post_index - 1]

    if current_post_index < len(all_posts) - 1:
        next_post = all_posts[current_post_index + 1]

    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'comments': comments,
        'form': form
    }

    if request.method == 'GET':
        post.counted_views += 1
        post.save()

    return render(request, 'myblog/blog-single.html', context)


def test(request):
    return render(request, 'myblog/test.html')


def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts': posts}
    return render(request, 'myblog/blog-home.html', context)


def blog_search(request):
    # print(request.__dict__)
    posts = Post.objects.filter(status=1)
    if request.method == "GET":
        # print("get request")
        s_query = request.GET.get('s')

        if s_query:
            posts = posts.filter(content__icontains=s_query)

    context = {'posts': posts}
    return render(request, 'myblog/blog-home.html', context)
