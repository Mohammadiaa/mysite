from django.urls import path
from myblog.views import *

app_name = "myblog"

urlpatterns = [
    path("", myblog_view, name = "index"),
    path("post/<int:pid>/", myblog_single, name = "single"),
    path("test/", test, name= "test")
]