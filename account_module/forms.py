from django import forms
from django.contrib.auth import login
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User


class LoginForm(forms.Form):
    name = forms.CharField(label='نام کاربری')
    password = forms.CharField(validators=[validators.MaxLengthValidator(100)], widget=forms.PasswordInput,
                               label='رمز عبور')


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(validators=[validators.MaxLengthValidator(100), validators.EmailValidator],
                             widget=forms.EmailInput, label='ایمیل')


class ResetPasswordForm(forms.Form):
    password = forms.CharField(validators=[validators.MaxLengthValidator(100)], widget=forms.PasswordInput,
                               label='رمز عبور')
    confirm_password = forms.CharField(
        error_messages={'confirm_error': {ValidationError: 'کلمه عبور با تکرار کلمه علور مغایزت دارد'}},
        validators=[validators.MaxLengthValidator(100)], widget=forms.PasswordInput,
        label='تکرار رمز عبور')


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar']



class EditUserPassForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور فعلی")
    new_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور جدید")
