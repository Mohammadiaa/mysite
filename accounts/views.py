from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CustomUserCreationForm 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
   
# درخواست فراموشی رمز عبور و ارسال لینک به ایمیل
def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        print("🔥 VIEW HIT")
        print(f"📧 EMAIL FROM FORM: {email}")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            # UIDb64 بساز
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))

            # Token بساز (TimestampSigner)
            signer = TimestampSigner()
            token = signer.sign(user.id)

            # لینک ریست
            reset_link = request.build_absolute_uri(
                reverse('accounts:reset_password', kwargs={'uidb64': uidb64, 'token': token})
            )

            # چاپ لینک تو ترمینال
            print(f"✅ USER FOUND: {user.username}")
            print(f"🔗 RESET LINK: {reset_link}")

        else:
            print("❌ USER NOT FOUND")

        return redirect('accounts:forgot_password_done')

    return render(request, 'accounts/forgotpass/password_reset_request.html')





# نمایش صفحه تایید ارسال ایمیل ریست پسورد
def password_reset_done(request):
     return render(request, 'accounts/forgotpass/password_reset_done.html')


# تایید توکن و نمایش فرم تغییر رمز جدید
def password_reset_confirm(request, uidb64, token):
    signer = TimestampSigner()
    user = None

    try:
        # decode base64
        user_id = force_str(urlsafe_base64_decode(uidb64))

        # validate token
        token_user_id = signer.unsign(token, max_age=3600)
        if str(user_id) != str(token_user_id):
            raise ValueError("Token does not match user ID")

        user = User.objects.get(id=user_id)

    except (BadSignature, SignatureExpired, User.DoesNotExist, ValueError):
        messages.error(request, "Invalid or expired password reset link.")
        return redirect('accounts:forgot_password')

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if password1 and password1 == password2:
            user.set_password(password1)
            user.save()
            messages.success(request, "Your password has been reset successfully.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'accounts/forgotpass/password_reset_confirm.html', {'user': user})




# نمایش صفحه تایید موفقیت‌آمیز تغییر رمز عبور
def password_reset_complete(request):
    return render(request, 'accounts/forgotpass/password_reset_complete.html')
    