from django.urls import path
from myblog.views import *

app_name = "myblog"

urlpatterns = [
    path("", myblog_view, name = "index"),
    path("single", myblog_single, name = "single")
]