from django.shortcuts import redirect
from django.views.generic import TemplateView
from member.dto.forms import LoginForm


class LoginPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

