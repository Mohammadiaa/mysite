from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse



# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                if user is not None:
                    login(request, user)
                    next_url = request.POST.get('next') or request.GET.get('next')
                    return redirect(next_url if next_url else '/myblog/')
                    

        if request.method != "POST": 
            form = AuthenticationForm()

        context = {'form': form}
        return render(request, 'accounts/login.html', context)
    else:
        return redirect('/')

    
@login_required    
def logout_view(request):
    logout(request)
    return redirect('/')

def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('accounts:login')) 
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    else:
        return redirect('/')
   