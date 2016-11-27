from django.conf.urls import url
from django.views.generic import TemplateView

from saytalk.views.web import TalkListPageView, PostViewSet, TalkDetailPageView, ChatDetailPageView

urlpatterns = [
    url(r'talk_list/$', TalkListPageView.as_view(), name='talk_list'),
    url(r'posting/$', PostViewSet.as_view({'post':'create'}), name='posting'),
    url(r'talk_detail/(?P<pk>[0-9]+)/$', TalkDetailPageView.as_view(), name='talk_detail'),
    url(r'chat_detail/(?P<pk>[0-9]+)/$', ChatDetailPageView.as_view(), name='chat_detail'),
    url(r'testing/$', TemplateView.as_view(template_name='base_test/say_talk/chat_video_stream.html'), name='testing'),
]
