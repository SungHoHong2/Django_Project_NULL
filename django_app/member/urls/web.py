from django.conf.urls import url
from member import views

urlpatterns = [
    url(r'^member/$', views.RegisterActionView.as_view({'post' : 'create'}), name='register'),
    url(r'^login/$', views.LoginActionView.as_view({'get': 'retrieve', 'post':'create'}), name='login'),
    url(r'^around_me/$', views.AroundMeView.as_view(), name='around_me'),
    url(r'^member_detail/(?P<pk>[0-9]+)/$', views.MemberDetailAction.as_view({'get':'retrieve'}), name='member_detail'),
    url(r'^profile/$', views.MyPageProfileView.as_view(), name='profile'),
]



