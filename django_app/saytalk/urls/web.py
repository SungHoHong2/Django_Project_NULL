from django.conf.urls import url
from saytalk.views.web import TalkListPageView, PostViewSet

urlpatterns = [
    url(r'talk_list/$', TalkListPageView.as_view(), name='talk_list'),
    url(r'posting/$', PostViewSet.as_view({'post':'create'}), name='posting'),

]
