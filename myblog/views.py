from django.shortcuts import render, get_object_or_404
from myblog.models import Post
from django.utils import timezone 

def myblog_view(request):
    now = timezone.now()
    posts = Post.objects.filter(status= 1, published_date__lte = now)
    context = {'Posts': posts} 
    return render(request, 'myblog/blog-home.html', context)

def myblog_single(request, pid):
    post = get_object_or_404(Post, id=pid, status=1, published_date__lte=timezone.now())
    
    post.counted_views += 1
    post.save()  

    context = {'post': post}
    return render(request, 'myblog/blog-single.html', context)