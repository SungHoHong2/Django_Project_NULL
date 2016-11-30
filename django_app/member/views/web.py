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

class LoginPageView(TemplateView):
    template_name = 'base_dev/index.html'

    def get_context_data(self, **kwargs):
        context = super(LoginPageView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.user.is_authenticated:
            return redirect('member:around_me')
        else:
            return self.render_to_response(context)


class LoginActionView(viewsets.ModelViewSet):
    # Login
    def create(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get('username'), password=request.data.get('password'))
        auth_login(request, user)
        #Token.objects.get_or_create(user=user)
        return redirect('/')

    # logout
    def retrieve(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('/')



class RegisterPageView(TemplateView):
    template_name = 'base_dev/register.html'

    def get_context_data(self, **kwargs):
        context = super(RegisterPageView, self).get_context_data(**kwargs)
        context['register_form'] = RegisterForm()
        context['register_image_form'] = RegisterImageForm()

        hash_tags = Hash_Tag.objects.all()
        hash_tags = [{ 'id' : tag.id, 'tag_name' : tag.tag_name } for tag in hash_tags]
        context['hash_tags'] = json.dumps(hash_tags)
        return context


class RegisterActionView(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication,CsrfExemptSessionAuthentication)

    #register
    def create(self, request, *args, **kwargs):

        myuser = MyUser.objects.create_user(
            username= request.data['username'],
            password = request.data['password'],
        )

        if request.data.get('image_file_ids') is not None:
            _index = 1
            for image_id in [x.strip() for x in request.data['image_file_ids'].split(',')]:
                img_obj = Image.objects.get(pk=image_id)
                img_obj.member = myuser
                img_obj.img_order = _index
                _index += 1
                img_obj.save()

        if request.data.get('hash_tag_ids') is not None:
            for hash_tag_id in [x.strip() for x in request.data['hash_tag_ids'].split(',')]:
                hash_tag = Hash_Tag.objects.get(id=hash_tag_id)
                Hash_Relationship.objects.create(member= myuser, hash_tag=hash_tag)

        #t1 = Token.objects.create(user=myuser)
        auth_login(request, myuser)
        return redirect('/')


class AroundMeView(TemplateView):
    template_name = 'base_test/around_me/member_list.html'

    def get_context_data(self, **kwargs):
        context = super(AroundMeView, self).get_context_data(**kwargs)
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
            "DESC LIMIT 10 "
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
        return context

def xstr(s):
    if s is None:
        return ''
    return str(s)


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



class MyPageProfileView(TemplateView):
    template_name = 'base_test/my_page/profile.html'

    def get_context_data(self, **kwargs):
        context = super(MyPageProfileView, self).get_context_data(**kwargs)
        return context
