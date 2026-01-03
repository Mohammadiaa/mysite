from django.urls import path
from myblog.views import *

app_name = "myblog"

urlpatterns = [
    path("", myblog_view, name = "index"),
    path("post/<int:pid>/", myblog_single, name = "single"),
    path('category/<str:cat_name>', myblog_view, name = "category"),
    path('author/<str:author_username>', myblog_view, name = "author"),
    path("test/", test, name= "test")
]