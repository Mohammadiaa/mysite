from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username_or_email = request.POST.get('username_or_email')
            password = request.POST.get('password')

            user = None

            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                try:
                   user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    user = None   

            if user is not None:
                user = authenticate(request, username=user.username, password=password)  
                if user is not None:
                    login(request, user)
                    next_url = request.POST.get('next') or request.GET.get('next')
                    return redirect(next_url if next_url else '/myblog/') 
                else:
                    messages.error(request, "Username/email or password is incorrect")
            else:
                messages.error(request, "Username/email or password is incorrect")
                
            form = AuthenticationForm()
            context = {'form': form}
            return render(request, 'accounts/login.html', context)
        else:
            form = AuthenticationForm()
            context = {'form': form}
            return render(request, 'accounts/login.html', context)      
    else:
        return redirect('/myblog/')      

    
@login_required    
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:login')) 
            else:
             print(form.errors) 
        form = CustomUserCreationForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('/')
   