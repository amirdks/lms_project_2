from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.views import View
from account_module.forms import LoginForm, ForgotPasswordForm, ResetPasswordForm, EditProfileModelForm, \
    EditUserPassForm
from account_module.models import User
from lesson_module.models import Lesson, SetHomeWork, HomeWorks
from lessons.models import FieldOfStudy, Base
from utils.email_service import send_email


class UserPanelView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest):
        user: User = request.user
        percent = 0
        if not user.is_teacher:
            field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
            base = Base.objects.filter(base_number=user.base.base_number).first()
            lessons = Lesson.objects.filter(is_active=True, base_id=base.id, field_of_study_id=field_of_study.id)
            set_home_works = SetHomeWork.objects.filter(lesson__field_of_study_id=user.field_of_study.id,
                                                        lesson__base_id=user.base.id, lesson__is_active=True).all()
            home_works = HomeWorks.objects.filter(user_id=user.id).all()
            percent = home_works.count() * 100 / set_home_works.count()
        context = {
            'percent_of_sent_homework': int(percent),
            'user': user
        }
        return render(request, 'account_module/user_panel.html', context)


class AnotherUserPanelView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest, id):
        user: User = User.objects.filter(id=id).first()
        percent = 0
        if not user.is_teacher:
            field_of_study = FieldOfStudy.objects.filter(id=user.field_of_study.id).first()
            base = Base.objects.filter(base_number=user.base.base_number).first()
            lessons = Lesson.objects.filter(is_active=True, base_id=base.id, field_of_study_id=field_of_study.id)
            set_home_works = SetHomeWork.objects.filter(lesson__field_of_study_id=user.field_of_study.id,
                                                        lesson__base_id=user.base.id, lesson__is_active=True).all()
            home_works = HomeWorks.objects.filter(user_id=user.id).all()
            if home_works:
                percent = home_works.count() * 100 / set_home_works.count()
            else:
                percent = 100
        context = {
            'percent_of_sent_homework': int(percent),
            'user': user
        }
        return render(request, 'account_module/another_user_panel.html', context)


class EditUserInfo(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'account_module/edit_user_info.html', context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            return redirect(reverse('user_panel_page'))

        context = {
            'form': edit_form,
            'current_user': current_user
        }
        return render(request, 'account_module/edit_user_info.html', context)


class EditUserPass(LoginRequiredMixin, View):
    login_url = reverse_lazy('login_page')

    def get(self, request: HttpRequest):
        user: User = User.objects.filter(id=request.user.id).first()
        form = EditUserPassForm()
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'account_module/edit_password.html', context)

    def post(self, request: HttpRequest):
        form = EditUserPassForm(request.POST)
        user: User = User.objects.filter(id=request.user.id).first()
        if form.is_valid():
            if user.check_password(form.cleaned_data.get('current_password')) and not form.cleaned_data.get(
                    'current_password') == form.cleaned_data.get('new_password'):
                user.set_password(form.cleaned_data.get('new_password'))
                user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')
                # messages.error(request, 'کلمه عبور وارد شده اشتباه می باشد')
        form = EditUserPassForm()
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'account_module/edit_password.html', context)


class LoginView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', context)

    def post(self, request: HttpRequest):

        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name_or_email = login_form.cleaned_data.get('name')
            user_password = login_form.cleaned_data.get('password')
            user = User.objects.filter(
                Q(username__exact=user_name_or_email) | Q(email__exact=user_name_or_email)).first()
            if user:
                is_password_correct = user.check_password(user_password)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('management_panel_page'))
                else:
                    login_form.add_error(field='password', error='کلمه عبور اشتباه است')
                    # messages.error(request, 'کلمه عبور اشتباه است')
            else:
                login_form.add_error(field='name', error='کاربری با مشخصات وارد شده یافت نشد')
                # messages.error(request, 'کاربری با مشخصات وارد شده یافت نشد')
        contex = {
            'login_form': login_form
        }
        return render(request, 'account_module/login_page.html', contex)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        forget_pass_form = ForgotPasswordForm()
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                # send_email(subject='بازیابی کلمه عبور', to=user.email, context={'user': user},
                #            template_name='templates/emails/forget-pass.html')
                send_email(subject='بازیابی کلمه عبور', to=user_email, context={'text': user.email_active_code},
                           template_name='contact/test_email.html')

                messages.success(request, 'یک لینک بازیابی با موفقیت به ایمیل شما ارسال شد')
            else:
                messages.error(request, 'ایمیل وارد شده یافت نشد')
        context = {'forget_pass_form': forget_pass_form}
        return render(request, 'account_module/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        elif request.user.is_authenticated:
            return redirect(reverse('lessons_list_page'))

        reset_pass_form = ResetPasswordForm()

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request: HttpRequest, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_pass_form.cleaned_data.get('password')
            confirm_pass = reset_pass_form.cleaned_data.get('confirm_password')
            if user_new_pass != confirm_pass:
                messages.error(request, 'رمز عبور با تکرار رمز عبور هماهنگی ندارد')
            else:

                user.set_password(user_new_pass)
                user.email_active_code = get_random_string(72)
                user.is_active = True
                user.save()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد')

        context = {
            'reset_pass_form': reset_pass_form,
            'user': user
        }

        return render(request, 'account_module/reset_password.html', context)


def user_panel_dashboard_component(request):
    return render(request, 'account_module/components/user_panel_dashboard_component.html')


def user_profile_component(request):
    return render(request, 'account_module/components/user_profile_component.html')
