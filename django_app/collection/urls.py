from django.conf.urls import url
from member import views
from collection.views import ImageActionView

urlpatterns = [
    url(r'^temp_image/$', ImageActionView.as_view({'post' : 'create'}), name='temp_image'),
]

