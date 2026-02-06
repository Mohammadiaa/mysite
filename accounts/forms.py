from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)


# فرم فراموشی رمز
class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="Enter your email", required=True)


# فرم تغییر رمز
class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(label="New password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirm new password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("new_password1")
        p2 = cleaned_data.get("new_password2")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
    
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label="Enter your email",
        max_length=254,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )