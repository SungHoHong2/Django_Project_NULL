from django.shortcuts import redirect
from django.views.generic import TemplateView
from member.dto.forms import LoginForm, RegisterForm, RegisterImageForm


class LoginPageView(TemplateView):
    template_name = 'base_test/index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

class RegisterPageView(TemplateView):
    template_name = 'base_test/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterPageView, self).get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        context['register_image_form'] = RegisterImageForm()
        return context