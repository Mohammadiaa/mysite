from django.shortcuts import render

def myblog_view(request):
    return render(request, 'myblog/blog-home.html')

def myblog_single(request):
    return render(request, 'myblog/blog-single.html')


