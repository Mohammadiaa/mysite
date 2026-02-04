from django.urls import path
from myblog.views import *
from .feeds import RssTutorialsFeeds


app_name = "myblog"

urlpatterns = [
    path("", myblog_view, name = "index"),
    path("post/<int:pid>/", myblog_single, name = "single"),
    path('category/<str:cat_name>', myblog_view, name = "category"),
    path('tag/<str:tag_name>', myblog_view, name = "tag"),
    path('author/<str:author_username>', myblog_view, name = "author"),
    path('search/', blog_search, name = 'search'),
    path('rss/feed', RssTutorialsFeeds(), name="rss_feed"),
    path("test/", test, name= "test"),
   
]