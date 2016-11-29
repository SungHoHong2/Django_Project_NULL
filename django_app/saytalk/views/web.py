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
            "SELECT "
                "ss.id, ss.title, ss.content, ci.img_file, hht.tag_names "
                "FROM saytalk_saytalk ss LEFT JOIN collection_image ci ON ci.say_talk_id = ss.id AND ci.img_order = 1 "
                "LEFT JOIN( "
                         "select chr.say_talk_id, string_agg(cht.tag_name, ', ') as tag_names "
                         "from collection_hash_tag cht "
                         "join collection_hash_relationship chr on chr.hash_tag_id = cht.id "
                         "group by chr.say_talk_id "
                ") hht on ss.id = hht.say_talk_id "
            "ORDER BY ss.created_date DESC "
            "LIMIT 16 "
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
            _list = [ {'id': row[0], 'title': row[1], 'content':row[2], 'img_file':settings.MEDIA_URL+xstr(row[3]), 'tag_names': row[4]}  for row in _list]
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
        myDict['created_by'] = request.user.id
        myDict['title'] = request.data['title']
        myDict['content'] = request.data['content']


        # if myDict.get('comment_type') is not None:
        #     myDict['is_parent'] = False



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
    template_name = 'base_test/say_talk/talk_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        _query_detail = (
            "select "
                    "ss.id, "
                    "ci.img_file as profile_img, "
                    "postimg.talk_images as talk_images, "
                    "ss.content as content, "
                    "ss.title as title, "
                    "chrs.tag_names as tag_names "
            "from saytalk_saytalk ss "
            "join member_myuser mm on ss.created_by != '' and mm.id = ss.created_by::Integer "
            "join collection_image ci on ci.member_id = mm.id and ci.img_order = 1 "
            "join( "
                "select "
                "ci2.say_talk_id, string_agg(ci2.img_file, ', ') as talk_images "
                "from collection_image ci2 "
            "where "
            "ci2.say_talk_id = %s "
            "group by ci2.say_talk_id "
        ") postimg on postimg.say_talk_id = ss.id "
        "join( "
            "select "
                "chr.say_talk_id, string_agg(c.tag_name, ', ') as tag_names "
                "from collection_hash_relationship chr "
            "join collection_hash_tag c on "
            "c.id = chr.hash_tag_id "
            "where chr.say_talk_id = %s "
            "group by say_talk_id "
        ") chrs on chrs.say_talk_id = ss.id "
        "where ss.id = %s "
        )

        with connection.cursor() as cursor:
            cursor.execute(_query_detail,[kwargs.get('pk'), kwargs.get('pk'), kwargs.get('pk')])
            _list = cursor.fetchall()
            _list = [ {'id': row[0],
                       'profile_img': settings.MEDIA_URL+xstr(row[1]),
                       'talk_img': row[2],
                       'content': row[3],
                       'title': row[4],
                       'tag_names': row[5],
                       }  for row in _list]
            context['talk_detail'] = json.dumps(_list)

        context['img_url'] = settings.MEDIA_URL
        context['comment_post'] = PostInsertForm()
        context['comment_img_post'] = PostImageForm()
        return context




class ChatDetailPageView(TemplateView):
    template_name = 'base_test/say_talk/chat_video_stream.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
