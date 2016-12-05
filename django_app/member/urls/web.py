from django.conf.urls import url
from member import views

urlpatterns = [
    # Register 화면 내용
    url(r'^member/$', views.RegisterActionView.as_view({'post' : 'create'}), name='register'),
    url(r'^login/$', views.LoginActionView.as_view({'get': 'retrieve', 'post':'create'}), name='login'),
    url(r'^nickname_duplicate/$', views.NicknameDuplicate.as_view({'post': 'create'}), name='nickname_duplicate'),

    # Around Me 기능
    url(r'^around_me/$', views.AroundMeView.as_view(), name='around_me'),
    url(r'^around_me_paging/$', views.AroundMePaging.as_view({'post':'create'}), name='around_me_paging'),
    url(r'^member_detail/(?P<pk>[0-9]+)/$', views.MemberDetailAction.as_view({'get':'retrieve', 'post':'create'}), name='member_detail'),
    url(r'^profile/$', views.MyPageProfileView.as_view(), name='profile'),
]



