import json

from django.conf import settings
from django.db import connection
from django.http import QueryDict
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from collection.models import Image, Hash_Tag, Hash_Relationship
from project_null.custom_authentication import CsrfExemptSessionAuthentication
from saytalk.dto.forms import PostInsertForm, PostImageForm
from saytalk.dto.serializer import SayTalkPostSerializer


class TalkListPageView(TemplateView):
    template_name = 'base_test/say_talk/talk_list.html'

    def get_context_data(self, **kwargs):
        context = super(TalkListPageView, self).get_context_data(**kwargs)
        context['post_form'] = PostInsertForm()
        context['image_form'] = PostImageForm()

        _query_talk = (
            "select ss.id, ss.title, ss.content, ci.img_file "
            "from saytalk_saytalk ss "
            "left join collection_image ci on ci.say_talk_id = ss.id and ci.img_order = 1 "
            "order by ss.created_date DESC "
            "limit 16 "
        )

        _query_hash = (
            "select "
            "    cht.id, cht.tag_name "
            "from member_myuser mm "
            "join collection_hash_relationship chr on chr.member_id = mm.id "
            "join collection_hash_tag cht on cht.id = chr.hash_tag_id "
            "where mm.id = %s "
        )

        with connection.cursor() as cursor:
            cursor.execute(_query_hash, [self.request.user.id])
            _list = cursor.fetchall()
            _list = [ {'id' : row[0], 'tag_name' : row[1] }  for row in _list]
            context['hash_tags'] = json.dumps(_list)

            cursor.execute(_query_talk,[])
            _list = cursor.fetchall()
            _list = [ {'id': row[0], 'title': row[1], 'content':row[2], 'img_file':settings.MEDIA_URL+xstr(row[3])}  for row in _list]
            context['talk_list'] = json.dumps(_list)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

def xstr(s):
    if s is None:
        return ''
    return str(s)


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = SayTalkPostSerializer
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        myDict = {}
        myDict['title'] = request.data['title']
        myDict['content'] = request.data['content']
        qdict = QueryDict('', mutable=True)
        qdict.update(myDict)

        serializer = self.get_serializer(data=qdict)
        serializer.is_valid(raise_exception=True)
        _say_talk = serializer.save()


        if request.data.get('image_file_ids') is not None:
            _index = 1
            for image_id in [x.strip() for x in request.data['image_file_ids'].split(',')]:
                img_obj = Image.objects.get(pk=image_id)
                img_obj.say_talk = _say_talk
                img_obj.img_order = _index
                _index += 1
                img_obj.save()

        if request.data.get('hash_tag_ids') is not None:
            for hash_tag_id in [x.strip() for x in request.data['hash_tag_ids'].split(',')]:
                hash_tag = Hash_Tag.objects.get(id=hash_tag_id)
                Hash_Relationship.objects.create(say_talk= _say_talk, hash_tag=hash_tag)
        return redirect('saytalk:talk_list')



class TalkDetailPageView(TemplateView):
    template_name = 'base_test/say_talk/talk_list.html'

    def get_context_data(self, **kwargs):
        context = super(TalkListPageView, self).get_context_data(**kwargs)
        context['post_form'] = PostInsertForm()
        context['image_form'] = PostImageForm()

        _query_talk = (
            "select ss.id, ss.title, ss.content, ci.img_file "
            "from saytalk_saytalk ss "
            "left join collection_image ci on ci.say_talk_id = ss.id and ci.img_order = 1 "
            "order by ss.created_date DESC "
            "limit 16 "
        )

        _query_hash = (
            "select "
            "    cht.id, cht.tag_name "
            "from member_myuser mm "
            "join collection_hash_relationship chr on chr.member_id = mm.id "
            "join collection_hash_tag cht on cht.id = chr.hash_tag_id "
            "where mm.id = %s "
        )

        with connection.cursor() as cursor:
            cursor.execute(_query_hash, [self.request.user.id])
            _list = cursor.fetchall()
            _list = [ {'id' : row[0], 'tag_name' : row[1] }  for row in _list]
            context['hash_tags'] = json.dumps(_list)

            cursor.execute(_query_talk,[])
            _list = cursor.fetchall()
            _list = [ {'id': row[0], 'title': row[1], 'content':row[2], 'img_file':settings.MEDIA_URL+xstr(row[3])}  for row in _list]
            context['talk_list'] = json.dumps(_list)

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
