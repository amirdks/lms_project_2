from django import forms
from django.contrib.auth import login
from django.core import validators
from django.core.exceptions import ValidationError

from account_module.models import User
from utils.password_strength_check import password_strength_check


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

    def clean_password(self):
        return password_strength_check(self.cleaned_data.get('password'))


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'address']


class EditUserPassForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور فعلی")
    new_password = forms.CharField(widget=forms.PasswordInput, label="رمز عبور جدید")

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get("current_password")
        new_password = cleaned_data.get("new_password")
        if current_password == new_password:
            raise forms.ValidationError('رمز عبور فعلی با رمز عبور جدید نمیتواند یکی باشد')

    def clean_new_password(self):
        return password_strength_check(self.cleaned_data.get('new_password'))
