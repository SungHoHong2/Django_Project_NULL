from django.conf.urls import url
from member.views import LoginPageView

urlpatterns = [
    url(r'^member/$', LoginPageView.as_view(), name='login'),
]
