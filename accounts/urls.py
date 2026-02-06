from django.urls import path
from accounts.views import *
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name = 'login'),
    path('logout', logout_view, name = 'logout'),
    path('signup/', signup_view, name = 'signup'),

    path('forgot-password/', views.password_reset_request, name='forgot_password'),
    path('forgot-password/done/', views.password_reset_done, name='forgot_password_done'),
    path('reset-password/<uidb64>/<token>/', views.password_reset_confirm, name='reset_password'),
    path('reset-password/done/', views.password_reset_complete, name='reset_password_done'),
]
