from django.conf.urls import url
from saytalk.views.web import TalkListPageView, PostViewSet, TalkDetailPageView

urlpatterns = [
    url(r'talk_list/$', TalkListPageView.as_view(), name='talk_list'),
    url(r'posting/$', PostViewSet.as_view({'post':'create'}), name='posting'),
    url(r'talk_detail/(?P<pk>[0-9]+)/$', TalkDetailPageView.as_view(), name='talk_detail'),

]
