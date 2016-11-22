"""project_null URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from member.views.web import LoginPageView, RegisterPageView
from django.views.generic import TemplateView


urlpatterns = [

    #url(r'^admin/', admin.site.urls),

    # 초기 화면 페이지 내용
    url(r'^$', LoginPageView.as_view(),name='main_login'),
    url(r'^about_us/$', TemplateView.as_view(template_name='base_test/about_us.html'), name='about_us'),
    url(r'^register/$', RegisterPageView.as_view(), name='register'),





    url(r'^member/', include('member.urls',namespace='member')),
]
