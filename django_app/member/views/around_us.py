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

class AroundMeView(TemplateView):
    template_name = 'base_dev/around_me/member_list.html'

    def get_context_data(self, **kwargs):
        context = super(AroundMeView, self).get_context_data(**kwargs)

        _total = len(MyUser.objects.all())
        _pagination = int(_total/6)


        _query = (
            "select "
                "mm.id as id "
              ", mm.username as username "
              ", ci.img_file as img_file "
              ", cch.tag_names as tag_names "
              ", mm.google_location as google_location "
              ", mlr.likes as likes "
            "from member_myuser mm "
            "left join (select "
                       "member_id, img_file "
                       "from collection_image where "
                       "img_order = 1 ) ci on ci.member_id = mm.id "
            "left join (select "
                      "chr.member_id, string_agg(cht.tag_name, ', ') as tag_names "
                      "from collection_hash_relationship chr "
                      "join collection_hash_tag cht on cht.id = chr.hash_tag_id "
                      "group by chr.member_id ) cch on cch.member_id = mm.id "
            "left join( select "
                      "mlr.followee_id, count(id) as likes "
                      "from member_like_relationship mlr "
                      "group by mlr.followee_id "
                     ") mlr on mlr.followee_id = mm.id "
            "order by mm.created_date "
            "DESC LIMIT 6 "
        )


        with connection.cursor() as cursor:
            cursor.execute(_query, [])
            _list = cursor.fetchall()
            _list = [ {'id' : row[0]
                      , 'username' : row[1]
                      , 'img_file' : settings.MEDIA_URL+xstr(row[2])
                      , 'tag_names' : row[3]
                      , 'google_location' : row[4]
                      , 'likes' : row[5] }  for row in _list
                      ]
            context['member_list'] = json.dumps(_list)
        context['pagination'] = _pagination
        return context




def xstr(s):
    if s is None:
        return ''
    return str(s)


class AroundMePaging(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):

        _query = (
            "select "
              "count(mm.id) OVER() as totalcount "
              ", mm.id as id "
              ", mm.username as username "
              ", ci.img_file as img_file "
              ", cch.tag_names as tag_names "
              ", mm.google_location as google_location "
              ", mlr.likes as likes "
            "from member_myuser mm "
            "left join (select "
                       "member_id, img_file "
                       "from collection_image where "
                       "img_order = 1 ) ci on ci.member_id = mm.id "
            "left join (select "
                      "chr.member_id, string_agg(cht.tag_name, ', ') as tag_names "
                      "from collection_hash_relationship chr "
                      "join collection_hash_tag cht on cht.id = chr.hash_tag_id "
                      "group by chr.member_id ) cch on cch.member_id = mm.id "
            "left join( select "
                      "mlr.followee_id, count(id) as likes "
                      "from member_like_relationship mlr "
                      "group by mlr.followee_id "
                     ") mlr on mlr.followee_id = mm.id "
        )

        print(self.request.data.get('paging'))
        _paging = int(self.request.data.get('paging')) * 6
        if request.data.get('search_like') is not None:
            _query += "where cch.tag_names like %s order by mm.created_date DESC OFFSET %s LIMIT 6"
            param_list = ['%'+str(request.data.get('search_like'))+'%', _paging ]
        else:
            _query += "order by mm.created_date DESC OFFSET %s LIMIT 6"
            param_list = [_paging ]


        with connection.cursor() as cursor:
            cursor.execute(_query, param_list)
            _list = cursor.fetchall()
            _list = [ { 'total_count':row[0]
                      , 'id' : row[1]
                      , 'username' : row[2]
                      , 'img_file' : settings.MEDIA_URL+xstr(row[3])
                      , 'tag_names' : row[4]
                      , 'google_location' : row[5]
                      , 'likes' : row[6] }  for row in _list
                      ]
            _member_list = json.dumps(_list)
        return Response(_member_list)



class MemberDetailAction(viewsets.ModelViewSet):
    # get Photo list
    serializer_class = ImageSerializer
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        image = Image.objects.all().filter(member_id=pk)
        serializer = self.get_serializer_class()
        _serializer = serializer(image, many=True)
        return Response(_serializer.data)

    def create(self, request, *args, **kwargs):
        followee_user = MyUser.objects.get(id= kwargs['pk'])
        follower_user = request.user
        lr = Like_Relationship.objects.create(followee= followee_user, follower=follower_user)
        return Response({ 'pk' : lr.pk})



