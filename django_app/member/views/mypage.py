from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from member.dto.forms import LoginForm, RegisterForm, RegisterImageForm
from project_null.custom_authentication import CsrfExemptSessionAuthentication
from member.models import MyUser, Like_Relationship
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
import json
from collection.models import Image, Hash_Tag, Hash_Relationship
from django.db import connection
from rest_framework.response import Response
from collection.serializer import ImageSerializer
from django.conf import settings


def xstr(s):
    if s is None:
        return ''
    return str(s)


class MyPageProfileView(TemplateView):
    template_name = 'base_test/my_page/profile.html'

    def get_context_data(self, **kwargs):
        context = super(MyPageProfileView, self).get_context_data(**kwargs)
        context['image'] =  json.dumps([{'id' : image.id, 'url': settings.MEDIA_URL+xstr(image.img_file)} for image in Image.objects.filter(member_id=self.request.user.id)])
        _query = (
            "select string_agg(cht.tag_name, ',') as tag_name from collection_hash_relationship chr "
            "join collection_hash_tag cht on cht.id = chr.hash_tag_id and chr.member_id = %s "
        )

        with connection.cursor() as cursor:
            cursor.execute(_query, [self.request.user.id])
            _object = cursor.fetchone()
            context['hash_tags'] = _object[0]
        return context
